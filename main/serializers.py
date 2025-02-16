from rest_framework import serializers
from .models import Product, Category, Brand, ProductAttribute, ProductAttributeValue, ProductReview

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug']

class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name')
    attribute_type = serializers.CharField(source='attribute.type')

    class Meta:
        model = ProductAttributeValue
        fields = ['attribute_name', 'attribute_type', 'value']

class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name')
    
    class Meta:
        model = ProductReview
        fields = ['user_name', 'rating', 'comment', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    attributes = ProductAttributeValueSerializer(source='attribute_values', many=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'stock_quantity', 'image', 'category', 'brand',
            'attributes', 'average_rating', 'reviews',
            'views_count', 'sales_count', 'created_at'
        ]

class ProductListSerializer(serializers.ModelSerializer):
    """Versiune simplificată pentru listare"""
    category_name = serializers.CharField(source='category.name')
    brand_name = serializers.CharField(source='brand.name', allow_null=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'stock_quantity',
            'image', 'category_name', 'brand_name', 'average_rating'
        ]

class AttributeFilterSerializer(serializers.ModelSerializer):
    """Serializator pentru opțiunile de filtrare disponibile"""
    values = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'type', 'values']
        
    def get_values(self, obj):
        """Returnează toate valorile unice pentru acest atribut"""
        return ProductAttributeValue.objects.filter(
            attribute=obj
        ).values_list('value', flat=True).distinct()
