from rest_framework import viewsets
from rest_framework import filters as drf_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db.models import Q, Min, Max
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .models import Product, Category, Brand, ProductAttribute
from .serializers import (
    ProductSerializer, ProductListSerializer, CategorySerializer,
    BrandSerializer, AttributeFilterSerializer
)

class ProductFilterSet(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = filters.CharFilter(field_name='category__slug')
    brand = filters.CharFilter(field_name='brand__slug')
    rating = filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    in_stock = filters.BooleanFilter(method='filter_in_stock')
    attributes = filters.CharFilter(method='filter_attributes')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'brand', 'rating', 'in_stock']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset

    def filter_attributes(self, queryset, name, value):
        """
        Filtrează produsele după atribute
        Format: color:red,blue;size:M,L
        """
        if not value:
            return queryset

        filters = Q()
        for attr_filter in value.split(';'):
            if ':' not in attr_filter:
                continue
            attr_name, values = attr_filter.split(':')
            attr_values = values.split(',')
            filters |= Q(
                attribute_values__attribute__name=attr_name,
                attribute_values__value__in=attr_values
            )
        return queryset.filter(filters).distinct()

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related(
        'category', 'brand'
    ).prefetch_related(
        'attribute_values', 'attribute_values__attribute',
        'reviews'
    )
    filterset_class = ProductFilterSet
    search_fields = ['name', 'description', 'category__name', 'brand__name']
    ordering_fields = ['price', 'created_at', 'average_rating', 'sales_count', 'views_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """Returnează opțiunile disponibile pentru filtrare"""
        cache_key = 'product_filter_options'
        options = cache.get(cache_key)

        if options is None:
            # Get price range
            price_range = Product.objects.filter(is_active=True).aggregate(
                min_price=Min('price'),
                max_price=Max('price')
            )

            # Get categories
            categories = Category.objects.filter(
                products__is_active=True
            ).distinct()

            # Get brands
            brands = Brand.objects.filter(
                products__is_active=True
            ).distinct()

            # Get filterable attributes
            attributes = ProductAttribute.objects.filter(
                is_filterable=True
            ).prefetch_related('productattributevalue_set')

            options = {
                'price_range': price_range,
                'categories': CategorySerializer(categories, many=True).data,
                'brands': BrandSerializer(brands, many=True).data,
                'attributes': AttributeFilterSerializer(attributes, many=True).data,
            }

            cache.set(cache_key, options, 60 * 15)  # Cache for 15 minutes

        return Response(options)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)
