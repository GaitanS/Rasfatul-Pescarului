from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'main'

# API Router
router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet, basename='product')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    # Home
    path('', views.home, name='home'),
    
    # Shop
    path('shop/', views.shop, name='shop'),
    path('shop/category/<slug:category_slug>/', views.shop, name='shop_category'),
    path('shop/product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/count/', views.cart_count, name='cart_count'),
    path('cart/total/', views.cart_total, name='cart_total'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    
    # Payment retry
    path('order/<int:order_id>/retry-payment/', views.retry_payment, name='retry_payment'),
    path('order/<int:order_id>/payment-status/', views.payment_status, name='payment_status'),
    
    # Locations
    path('locations/', views.fishing_locations, name='fishing_locations'),
    path('locations/map/', views.locations_map, name='locations_map'),
    path('locations/filter/', views.filter_lakes, name='filter_lakes'),
    path('api/nearby-lakes/', views.nearby_lakes, name='nearby_lakes'),
    path('locations/county/<slug:county_slug>/', views.county_lakes, name='county_lakes'),
    path('locations/lake/<int:lake_id>/', views.lake_detail, name='lake_detail'),
    
    # Tutorials
    path('tutorials/', views.tutorials, name='tutorials'),
    path('tutorials/<int:video_id>/', views.video_detail, name='video_detail'),
    
    # Account
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Orders
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    
    # Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('api/solunar-data/', views.solunar_data, name='solunar_data'),
    path('solunar-calendar/', views.solunar_calendar, name='solunar_calendar'),
    path('terms/', views.terms, name='terms'),
]
