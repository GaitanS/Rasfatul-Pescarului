import json
import datetime
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
import stripe
from .models import (
    Product, Category, Lake, County, Video, Order, OrderItem,
    Brand, ProductAttribute, ProductAttributeValue
)
from .utils.tokens import account_activation_token, password_reset_token
from .utils.email import (
    send_verification_email, send_password_reset_email,
    send_contact_confirmation_email, send_contact_admin_email,
    send_order_cancelled_email, send_order_cancelled_admin_email
)


import json
import datetime
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Min, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    Product, Category, Lake, County, Video, Order, OrderItem,
    Brand, ProductAttribute, ProductAttributeValue
)

def home(request):
    """View pentru pagina principală"""
    return render(request, 'index/index.html')

def shop(request, category_slug=None):
    """View pentru pagina de magazin"""
    # Get base queryset
    products = Product.objects.filter(is_active=True).select_related(
        'category', 'brand'
    ).prefetch_related(
        'attribute_values', 'attribute_values__attribute'
    )
    
    # Get all active categories and brands for filters
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(products__is_active=True).distinct()
    
    # Get price range for the price slider
    price_range = products.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )
    
    # Get filterable attributes
    attributes = ProductAttribute.objects.filter(is_filterable=True)
    
    # Apply category filter
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if category.parent:
            products = products.filter(category=category)
        else:
            # If it's a parent category, include all its subcategories
            subcategories = category.get_all_children()
            subcategory_ids = [cat.id for cat in subcategories]
            subcategory_ids.append(category.id)
            products = products.filter(category_id__in=subcategory_ids)
    
    # Apply search filter
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    # Apply brand filter
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    
    # Apply price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Apply rating filter
    min_rating = request.GET.get('rating')
    if min_rating:
        products = products.filter(average_rating__gte=min_rating)
    
    # Apply stock filter
    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = products.filter(stock_quantity__gt=0)
    
    # Apply attribute filters
    attributes_filter = request.GET.get('attributes')
    if attributes_filter:
        for attr_filter in attributes_filter.split(';'):
            if ':' in attr_filter:
                attr_name, values = attr_filter.split(':')
                attr_values = values.split(',')
                products = products.filter(
                    attribute_values__attribute__name=attr_name,
                    attribute_values__value__in=attr_values
                ).distinct()
    
    # Apply sorting
    sort_by = request.GET.get('ordering', '-created_at')
    if sort_by in ['price', '-price', '-average_rating', '-sales_count', '-created_at']:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'category': category,
        'categories': categories,
        'brands': brands,
        'attributes': attributes,
        'price_range': price_range,
        'search_query': search_query
    }
    return render(request, 'shop/list.html', context)

def product_detail(request, slug):
    """View pentru detaliile unui produs"""
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand')
        .prefetch_related(
            'attribute_values',
            'attribute_values__attribute',
            'reviews'
        ),
        slug=slug,
        is_active=True
    )
    
    # Get related products
    related_products = Product.objects.filter(
        Q(category=product.category) | Q(brand=product.brand),
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }

def cart(request):
    """View pentru coșul de cumpărături"""
    return render(request, 'shop/cart.html')

@require_http_methods(['POST'])
@csrf_exempt
def add_to_cart(request):
    """Adaugă un produs în coș"""
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    if not request.session.get('cart'):
        request.session['cart'] = {}
    
    cart = request.session['cart']
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    request.session.modified = True
    return JsonResponse({'status': 'success'})

@require_http_methods(['POST'])
@csrf_exempt
def update_cart(request):
    """Actualizează cantitatea unui produs din coș"""
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 0))
    
    if request.session.get('cart') and product_id in request.session['cart']:
        if quantity > 0:
            request.session['cart'][product_id] = quantity
        else:
            del request.session['cart'][product_id]
        request.session.modified = True
    
    return JsonResponse({'status': 'success'})

@require_http_methods(['POST'])
@csrf_exempt
def remove_from_cart(request):
    """Șterge un produs din coș"""
    data = json.loads(request.body)
    product_id = data.get('product_id')
    
    if request.session.get('cart') and product_id in request.session['cart']:
        del request.session['cart'][product_id]
        request.session.modified = True
    
    return JsonResponse({'status': 'success'})

def cart_count(request):
    """Returnează numărul de produse din coș"""
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return JsonResponse({'count': count})

def cart_total(request):
    """Calculează totalul coșului"""
    cart = request.session.get('cart', {})
    total = Decimal('0.00')
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            total += product.price * Decimal(str(quantity))
        except Product.DoesNotExist:
            pass
    
    return JsonResponse({'total': str(total)})

    return render(request, 'shop/detail.html', context)

@login_required
def checkout(request):
    """View pentru procesul de checkout"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Coșul tău este gol.')
        return redirect('main:cart')
    
    # Calculate cart total
    total = Decimal('0.00')
    items = []
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            total += product.price * Decimal(str(quantity))
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * Decimal(str(quantity))
            })
        except Product.DoesNotExist:
            pass
    
    context = {
        'items': items,
        'total': total
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def checkout_success(request):
    """View pentru pagina de succes după checkout"""
    # Clear the cart after successful checkout
    if 'cart' in request.session:
        del request.session['cart']
    return render(request, 'shop/checkout_success.html')

@csrf_exempt
def stripe_webhook(request):
    """Handler pentru webhook-urile Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        fulfill_order(session)
    
    return HttpResponse(status=200)





@login_required
def retry_payment(request, order_id):
    """View pentru reîncercarea plății unui order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(request, 'Această comandă nu poate fi replătită.')
        return redirect('main:order_detail', order_id=order.id)
    
    # Create new payment session
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'ron',
                    'unit_amount': int(order.total * 100),
                    'product_data': {
                        'name': f'Order #{order.id}',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('main:checkout_success')
            ),
            cancel_url=request.build_absolute_uri(
                reverse('main:order_detail', args=[order.id])
            ),
            metadata={
                'order_id': order.id
            }
        )
        return redirect(checkout_session.url)
    except Exception as e:
        messages.error(request, 'A apărut o eroare la procesarea plății.')
        return redirect('main:order_detail', order_id=order.id)

@login_required
def payment_status(request, order_id):
    """View pentru verificarea statusului plății"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return JsonResponse({
        'status': order.status,
        'paid': order.is_paid
    })


def fishing_locations(request):
    """View pentru lista de locații de pescuit"""
    counties = County.objects.all().order_by('name')
    return render(request, 'locations/list.html', {'counties': counties})

def locations_map(request):
    """View pentru harta locațiilor"""
    lakes = Lake.objects.filter(is_active=True).select_related('county')
    return render(request, 'locations/map.html', {'lakes': lakes})

def county_lakes(request, county_slug):
    """View pentru lacurile dintr-un județ"""
    county = get_object_or_404(County, slug=county_slug)
    lakes = Lake.objects.filter(county=county, is_active=True)
    return render(request, 'locations/county_lakes.html', {
        'county': county,
        'lakes': lakes
    })

def lake_detail(request, lake_id):
    """View pentru detaliile unui lac"""
    lake = get_object_or_404(Lake, id=lake_id, is_active=True)
    return render(request, 'locations/lake_detail.html', {'lake': lake})


def tutorials(request):
    """View pentru lista de tutoriale video"""
    videos = Video.objects.filter(is_active=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    
    return render(request, 'tutorials/list.html', {'videos': videos})

def video_detail(request, video_id):
    """View pentru detaliile unui tutorial video"""
    video = get_object_or_404(Video, id=video_id, is_active=True)
    
    # Get related videos
    related_videos = Video.objects.filter(
        is_active=True
    ).exclude(id=video.id).order_by('?')[:4]
    
    return render(request, 'tutorials/detail.html', {
        'video': video,
        'related_videos': related_videos
    })


def login_view(request):
    """View pentru autentificare"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'main:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Email sau parolă incorectă.')
    
    return render(request, 'account/login.html')

def register(request):
    """View pentru înregistrare"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Parolele nu coincid.')
        else:
            try:
                user = User.objects.create_user(email, email, password1)
                user.is_active = False
                user.save()
                
                # Send verification email
                send_verification_email(request, user)
                
                messages.success(
                    request,
                    'Cont creat cu succes! Verifică email-ul pentru activare.'
                )
                return redirect('main:login')
            except Exception as e:
                messages.error(request, 'Eroare la crearea contului.')
    
    return render(request, 'account/register.html')

def verify_email(request, uidb64, token):
    """View pentru verificarea email-ului"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email verificat cu succes! Te poți autentifica.')
    else:
        messages.error(request, 'Link de verificare invalid.')
    
    return redirect('main:login')

def password_reset(request):
    """View pentru resetarea parolei"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Send password reset email
            send_password_reset_email(request, user)
            messages.success(
                request,
                'Email trimis cu instrucțiuni de resetare a parolei.'
            )
            return redirect('main:login')
        except User.DoesNotExist:
            messages.error(request, 'Nu există cont cu acest email.')
    
    return render(request, 'account/password_reset.html')

def password_reset_confirm(request, uidb64, token):
    """View pentru confirmarea resetării parolei"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and password_reset_token.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 != password2:
                messages.error(request, 'Parolele nu coincid.')
            else:
                user.set_password(password1)
                user.save()
                messages.success(
                    request,
                    'Parola a fost resetată cu succes! Te poți autentifica.'
                )
                return redirect('main:login')
        
        return render(request, 'account/password_reset_confirm.html')
    else:
        messages.error(request, 'Link de resetare invalid.')
        return redirect('main:login')

@login_required
def logout_view(request):
    """View pentru delogare"""
    logout(request)
    return redirect('main:home')

@login_required
def profile(request):
    """View pentru profilul utilizatorului"""
    return render(request, 'account/profile.html')

@login_required
def edit_profile(request):
    """View pentru editarea profilului"""
    if request.method == 'POST':
        try:
            profile = request.user.profile
            profile.phone = request.POST.get('phone')
            profile.address = request.POST.get('address')
            profile.save()
            
            messages.success(request, 'Profil actualizat cu succes!')
            return redirect('main:profile')
        except Exception as e:
            messages.error(request, 'Eroare la actualizarea profilului.')
    
    return render(request, 'account/edit_profile.html')

@login_required
def change_password(request):
    """View pentru schimbarea parolei"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Parola veche este incorectă.')
        elif password1 != password2:
            messages.error(request, 'Parolele noi nu coincid.')
        else:
            request.user.set_password(password1)
            request.user.save()
            messages.success(request, 'Parola a fost schimbată cu succes!')
            return redirect('main:login')
    
    return render(request, 'account/change_password.html')


@login_required
def orders(request):
    """View pentru lista comenzilor utilizatorului"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'account/orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """View pentru detaliile unei comenzi"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'account/order_detail.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    """View pentru anularea unei comenzi"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(request, 'Această comandă nu poate fi anulată.')
        return redirect('main:order_detail', order_id=order.id)
    
    order.status = 'cancelled'
    order.save()
    
    # Send cancellation emails
    send_order_cancelled_email(request, order)
    send_order_cancelled_admin_email(order)
    
    messages.success(request, 'Comanda a fost anulată cu succes.')
    return render(request, 'account/order_cancel_confirmation.html', {
        'order': order
    })


def about(request):
    """View pentru pagina Despre noi"""
    return render(request, 'pages/about.html')

def contact(request):
    """View pentru pagina de contact"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        try:
            # Send contact emails
            send_contact_confirmation_email(email, name)
            send_contact_admin_email(name, email, message)
            
            messages.success(
                request,
                'Mesajul tău a fost trimis cu succes! Te vom contacta în curând.'
            )
            return redirect('main:contact')
        except Exception as e:
            messages.error(
                request,
                'A apărut o eroare la trimiterea mesajului. Te rugăm să încerci din nou.'
            )
    
    return render(request, 'pages/contact.html')

def terms(request):
    """View pentru pagina de termeni și condiții"""
    return render(request, 'pages/terms.html')
