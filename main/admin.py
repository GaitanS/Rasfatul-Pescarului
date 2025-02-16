from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg
from .models import (
    Category, Product, County, Lake, Video, 
    Testimonial, Order, OrderItem, Profile, 
    SiteSettings, Payment, Brand, ProductAttribute,
    ProductAttributeValue, ProductReview
)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('parent',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_filterable')
    list_filter = ('type', 'is_filterable')
    search_fields = ('name',)

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ('created_at',)
    can_delete = False

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock_quantity', 
                   'average_rating', 'views_count', 'sales_count', 'is_featured', 'is_active')
    list_filter = ('category', 'brand', 'is_featured', 'is_active')
    search_fields = ('name', 'description', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock_quantity', 'is_featured', 'is_active')
    inlines = [ProductAttributeValueInline, ProductReviewInline]
    readonly_fields = ('views_count', 'sales_count', 'average_rating')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Categorization', {
            'fields': ('category', 'brand')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Statistics', {
            'fields': ('views_count', 'sales_count', 'average_rating'),
            'classes': ('collapse',)
        })
    )

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name', 'user__email', 'comment')
    raw_id_fields = ('product', 'user')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        for review in queryset:
            review.product.update_rating()
    approve_reviews.short_description = "Aprobă review-urile selectate"

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Lake)
class LakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'county', 'is_featured', 'is_active')
    list_filter = ('county', 'is_featured', 'is_active')
    search_fields = ('name', 'description', 'fish_species')
    list_editable = ('is_featured', 'is_active')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'description')
    list_editable = ('is_featured', 'is_active')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'role', 'content')
    list_editable = ('is_active',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'status', 'payment_method', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('id', 'user__email', 'full_name', 'email', 'phone')
    readonly_fields = ('subtotal', 'total_amount')
    inlines = [OrderItemInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'county', 'is_email_verified')
    list_filter = ('is_email_verified', 'newsletter', 'order_updates')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone', 'city')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'county')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_link', 'payment_method', 'amount', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('order__id', 'transaction_id', 'order__user__email')
    readonly_fields = ('order', 'payment_method', 'transaction_id', 'amount', 'created_at')

    def order_link(self, obj):
        url = f"/admin/main/order/{obj.order.id}/change/"
        return format_html('<a href="{}">{}</a>', url, f'Comandă #{obj.order.id}')
    order_link.short_description = 'Comandă'

    def has_add_permission(self, request):
        return False  # Payments should only be created through the payment process

    def has_delete_permission(self, request, obj=None):
        return False  # Payments should not be deletable for audit purposes
