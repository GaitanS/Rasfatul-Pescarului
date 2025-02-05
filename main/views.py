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
from .models import Product, Category, Lake, County, Video, Order, OrderItem

def home(request):
    """View pentru pagina principală"""
    return render(request, 'index/index.html')

def shop(request, category_slug=None):
    """View pentru pagina de magazin"""
    products = Product.objects.filter(is_active=True)
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/list.html', {'products': products, 'category': category})

def product_detail(request, slug):
    """View pentru detalii produs"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'shop/detail.html', {'product': product})

def cart(request):
    """View pentru coșul de cumpărături"""
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
        request.session['cart'] = cart
    
    # Convert old format cart items to new format
    updated = False
    for product_id, item_data in list(cart.items()):
        if isinstance(item_data, (int, str)):
            try:
                product = get_object_or_404(Product, id=int(product_id))
                cart[product_id] = {
                    'quantity': int(item_data),
                    'price': str(product.price)
                }
                updated = True
            except (ValueError, Product.DoesNotExist):
                del cart[product_id]
                updated = True
    
    if updated:
        request.session.modified = True
    
    # Process cart items
    cart_items = []
    cart_total = Decimal('0.00')

    for product_id, item_data in list(cart.items()):
        try:
            if not isinstance(item_data, dict) or 'quantity' not in item_data or 'price' not in item_data:
                del cart[product_id]
                continue
                
            product = get_object_or_404(Product, id=int(product_id))
            quantity = int(item_data['quantity'])
            price = Decimal(item_data['price'])
            total = price * quantity
            cart_total += total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total': total
            })
        except (ValueError, Product.DoesNotExist):
            del cart[product_id]

    shipping_cost = Decimal('20.00') if cart_total < Decimal('200.00') else Decimal('0.00')
    total_with_shipping = cart_total + shipping_cost

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_cost': shipping_cost,
        'total_with_shipping': total_with_shipping,
    }
    return render(request, 'shop/cart.html', context)

@require_http_methods(["POST"])
def add_to_cart(request):
    """API endpoint pentru adăugare în coș"""
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        # Get product to access its price
        product = get_object_or_404(Product, id=product_id)
        
        if not request.session.get('cart'):
            request.session['cart'] = {}
        
        cart = request.session['cart']
        
        # If product already in cart, update quantity
        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            # Add new product to cart with quantity and price
            cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price)
            }
        
        request.session.modified = True
        
        # Get the return URL, defaulting to the shop page
        next_url = request.POST.get('next')
        if not next_url:
            next_url = request.META.get('HTTP_REFERER')
        if not next_url:
            next_url = reverse('main:shop')
            
        messages.success(request, f'{product.name} a fost adăugat în coș.')
        return redirect(next_url)
        
    except ValueError:
        messages.error(request, 'Cantitate invalidă.')
        return redirect('main:shop')
    except Exception as e:
        messages.error(request, f'Eroare la adăugarea în coș: {str(e)}')
        return redirect('main:shop')

@require_http_methods(["POST"])
def update_cart(request):
    """API endpoint pentru actualizare coș"""
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        
        if request.session.get('cart'):
            cart = request.session['cart']
            if quantity > 0:
                # Get product to access its price
                product = get_object_or_404(Product, id=product_id)
                if product_id in cart:
                    cart[product_id]['quantity'] = quantity
                    messages.success(request, f'Cantitatea pentru {product.name} a fost actualizată.')
                else:
                    cart[product_id] = {
                        'quantity': quantity,
                        'price': str(product.price)
                    }
                    messages.success(request, f'{product.name} a fost adăugat în coș.')
            else:
                if product_id in cart:
                    product = get_object_or_404(Product, id=product_id)
                    cart.pop(product_id, None)
                    messages.success(request, f'{product.name} a fost eliminat din coș.')
            request.session.modified = True
        
        # Get the return URL, defaulting to the cart page
        next_url = request.POST.get('next')
        if not next_url:
            next_url = request.META.get('HTTP_REFERER')
        if not next_url:
            next_url = reverse('main:cart')
            
        return redirect(next_url)
        
    except ValueError:
        messages.error(request, 'Cantitate invalidă.')
        return redirect('main:cart')
    except Exception as e:
        messages.error(request, f'Eroare la actualizarea coșului: {str(e)}')
        return redirect('main:cart')

@require_http_methods(["POST"])
def remove_from_cart(request):
    """API endpoint pentru eliminare din coș"""
    try:
        product_id = request.POST.get('product_id')
        
        if request.session.get('cart'):
            cart = request.session['cart']
            if product_id in cart:
                # Get product name for the message
                product = get_object_or_404(Product, id=product_id)
                cart.pop(product_id, None)
                request.session.modified = True
                messages.success(request, f'{product.name} a fost eliminat din coș.')
        
        # Get the return URL, defaulting to the cart page
        next_url = request.POST.get('next')
        if not next_url:
            next_url = request.META.get('HTTP_REFERER')
        if not next_url:
            next_url = reverse('main:cart')
            
        return redirect(next_url)
        
    except Exception as e:
        messages.error(request, f'Eroare la eliminarea din coș: {str(e)}')
        return redirect('main:cart')

def cart_count(request):
    """API endpoint pentru numărul de produse din coș"""
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
        request.session['cart'] = cart
    
    count = 0
    for item_data in cart.values():
        try:
            if isinstance(item_data, dict) and 'quantity' in item_data:
                count += int(item_data['quantity'])
            elif isinstance(item_data, (int, str)):
                count += int(item_data)
        except (ValueError, TypeError):
            continue
            
    return JsonResponse({'count': count})

def cart_total(request):
    """API endpoint pentru totalul coșului"""
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
        request.session['cart'] = cart
    
    total = Decimal('0.00')
    updated = False
    
    for product_id, item_data in list(cart.items()):
        try:
            if isinstance(item_data, dict) and 'quantity' in item_data and 'price' in item_data:
                quantity = int(item_data['quantity'])
                price = Decimal(item_data['price'])
                total += price * quantity
            elif isinstance(item_data, (int, str)):
                # Convert old format to new format
                product = get_object_or_404(Product, id=int(product_id))
                quantity = int(item_data)
                price = product.price
                total += price * quantity
                # Update cart with new format
                cart[product_id] = {
                    'quantity': quantity,
                    'price': str(price)
                }
                updated = True
        except (ValueError, TypeError, Product.DoesNotExist):
            del cart[product_id]
            updated = True
            continue
    
    if updated:
        request.session.modified = True
        
    return JsonResponse({'total': str(total)})

@login_required
def checkout(request):
    """View pentru checkout"""
    return render(request, 'shop/checkout.html')

def checkout_success(request):
    """View pentru succes checkout"""
    return render(request, 'shop/checkout_success.html')

@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    """Webhook pentru Stripe"""
    if not request.body:
        return JsonResponse({'error': 'Empty request body'}, status=400)
        
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    try:
        event_type = payload.get('type')
        if not event_type:
            return JsonResponse({'error': 'Missing event type'}, status=400)
        
        # Handle different event types
        if event_type == 'payment_intent.succeeded':
            # Handle successful payment
            pass
        elif event_type == 'payment_intent.payment_failed':
            # Handle failed payment
            pass
            
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def retry_payment(request, order_id):
    """View pentru reîncercarea plății"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/stripe_payment.html', {'order': order})

def payment_status(request, order_id):
    """API endpoint pentru status plată"""
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({'status': order.status})

def fishing_locations(request):
    """View pentru locații de pescuit"""
    return render(request, 'locations/list.html')

def locations_map(request):
    """View pentru harta locațiilor"""
    return render(request, 'locations/map.html')

def county_lakes(request, county_slug):
    """View pentru lacurile dintr-un județ"""
    county = get_object_or_404(County, slug=county_slug)
    lakes = Lake.objects.filter(county=county)
    return render(request, 'locations/county_lakes.html', {'county': county, 'lakes': lakes})

def lake_detail(request, lake_id):
    """View pentru detalii lac"""
    lake = get_object_or_404(Lake, id=lake_id)
    return render(request, 'locations/lake_detail.html', {'lake': lake})

def tutorials(request):
    """View pentru tutoriale"""
    videos = Video.objects.filter(is_active=True)
    return render(request, 'tutorials/list.html', {'videos': videos})

def video_detail(request, video_id):
    """View pentru detalii video"""
    video = get_object_or_404(Video, id=video_id, is_active=True)
    return render(request, 'tutorials/detail.html', {'video': video})

from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

def login_view(request):
    """View pentru login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        # Check login attempts
        attempts_key = f'login_attempts_{username}'
        attempts = cache.get(attempts_key, 0)
        
        if attempts >= 5:  # Max 5 attempts
            lockout_time = cache.ttl(attempts_key)
            if lockout_time:
                minutes = (lockout_time + 59) // 60  # Round up to nearest minute
                messages.error(
                    request,
                    f'Prea multe încercări eșuate. Încercați din nou în {minutes} minute.'
                )
                return render(request, 'account/login.html')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Check if email is verified
            if not user.profile.is_email_verified:
                messages.error(
                    request,
                    'Contul nu este activat. Vă rugăm să verificați email-ul pentru a activa contul.'
                )
                return render(request, 'account/login.html')
            
            # Reset login attempts on successful login
            cache.delete(attempts_key)
            
            # Set session expiry based on "Remember me"
            if remember:
                request.session.set_expiry(timedelta(days=30))
            else:
                request.session.set_expiry(0)  # Expires when browser closes
                
            login(request, user)
            
            # Get the next URL from POST or query string
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('main:home')
        
        # Increment failed login attempts
        cache.set(attempts_key, attempts + 1, timeout=300)  # 5 minutes timeout
        
        if attempts >= 4:  # Show warning on 5th attempt
            messages.warning(
                request,
                'Următoarea încercare eșuată va bloca contul pentru 5 minute.'
            )
        
        messages.error(request, 'Credențiale invalide')
    return render(request, 'account/login.html')

import requests
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.conf import settings
from .utils.tokens import email_verification_token
from .utils.email import send_email

def register(request):
    """View pentru înregistrare"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone', '')
        county_id = request.POST.get('county', '')
        terms = request.POST.get('terms', False)
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Validate reCAPTCHA
        recaptcha_success = False
        if recaptcha_response:
            try:
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', {
                    'secret': settings.RECAPTCHA_PRIVATE_KEY,
                    'response': recaptcha_response
                })
                result = r.json()
                recaptcha_success = result.get('success', False)
            except:
                messages.error(request, 'Eroare la validarea reCAPTCHA. Încercați din nou.')
                return render(request, 'account/register.html', {'form_data': request.POST})

        if not recaptcha_success:
            messages.error(request, 'Vă rugăm să confirmați că nu sunteți robot.')
            return render(request, 'account/register.html', {'form_data': request.POST})

        # Basic validation
        if not all([first_name, last_name, email, password, confirm_password]):
            messages.error(request, 'Toate câmpurile obligatorii trebuie completate.')
            return render(request, 'account/register.html', {'form_data': request.POST})

        if not terms:
            messages.error(request, 'Trebuie să acceptați termenii și condițiile.')
            return render(request, 'account/register.html', {'form_data': request.POST})

        if password != confirm_password:
            messages.error(request, 'Parolele nu coincid.')
            return render(request, 'account/register.html', {'form_data': request.POST})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Există deja un cont cu această adresă de email.')
            return render(request, 'account/register.html', {'form_data': request.POST})

        try:
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create or update profile
            profile = user.profile
            profile.phone = phone
            if county_id:
                try:
                    county = County.objects.get(id=county_id)
                    profile.county = county
                except County.DoesNotExist:
                    pass
            profile.save()

            # Generate verification token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user)
            verification_url = f"{settings.SITE_URL}{reverse('main:verify_email', args=[uid, token])}"

            # Send verification email
            send_email(
                to_email=user.email,
                subject='Verificare adresă email - Răsfățul Pescarului',
                template='emails/verify_email.html',
                context={
                    'name': user.get_full_name(),
                    'verification_url': verification_url
                }
            )

            messages.success(
                request,
                'Contul a fost creat cu succes! Vă rugăm să verificați email-ul pentru a activa contul.'
            )
            return redirect('main:login')

        except Exception as e:
            messages.error(request, f'Eroare la crearea contului: {str(e)}')
            return render(request, 'account/register.html', {'form_data': request.POST})

    # GET request
    counties = County.objects.all().order_by('name')
    return render(request, 'account/register.html', {
        'counties': counties,
        'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY
    })

def verify_email(request, uidb64, token):
    """View pentru verificare email"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.profile.is_email_verified = True
        user.profile.save()
        messages.success(request, 'Email-ul a fost verificat cu succes! Vă puteți autentifica.')
    else:
        messages.error(request, 'Link-ul de verificare este invalid sau a expirat.')

    return redirect('main:login')

def logout_view(request):
    """View pentru logout"""
    logout(request)
    return redirect('main:home')

@login_required
def profile(request):
    """View pentru profil"""
    return render(request, 'account/profile.html')

@login_required
def edit_profile(request):
    """View pentru editare profil"""
    return render(request, 'account/edit_profile.html')

@login_required
def change_password(request):
    """View pentru schimbare parolă"""
    return render(request, 'account/change_password.html')

@login_required
def orders(request):
    """View pentru comenzi"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """View pentru detalii comandă"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'account/order_detail.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    """View pentru anulare comandă"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status = 'cancelled'
    order.save()
    return render(request, 'account/order_cancel_confirmation.html', {'order': order})

def about(request):
    """View pentru despre noi"""
    return render(request, 'pages/about.html')

def contact(request):
    """View pentru contact"""
    return render(request, 'pages/contact.html')

def terms(request):
    """View pentru termeni și condiții"""
    return render(request, 'pages/terms.html')

def password_reset(request):
    """View pentru solicitare resetare parolă"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user)
            reset_url = f"{settings.SITE_URL}{reverse('main:password_reset_confirm', args=[uid, token])}"
            
            # Send reset email
            send_email(
                to_email=user.email,
                subject='Resetare parolă - Răsfățul Pescarului',
                template='emails/password_reset.html',
                context={
                    'name': user.get_full_name(),
                    'reset_url': reset_url
                }
            )
            
            messages.success(
                request,
                'Am trimis un email cu instrucțiuni pentru resetarea parolei.'
            )
            return redirect('main:login')
            
        except User.DoesNotExist:
            # Don't reveal that the email doesn't exist
            messages.success(
                request,
                'Dacă există un cont asociat acestei adrese de email, veți primi instrucțiuni pentru resetarea parolei.'
            )
            return redirect('main:login')
            
    return render(request, 'account/password_reset.html')

def password_reset_confirm(request, uidb64, token):
    """View pentru confirmare resetare parolă"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and email_verification_token.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                messages.error(request, 'Parolele nu coincid.')
                return render(request, 'account/password_reset_confirm.html', {'validlink': True})
                
            # Set new password
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Parola a fost schimbată cu succes! Vă puteți autentifica.')
            return redirect('main:login')
            
        return render(request, 'account/password_reset_confirm.html', {'validlink': True})
        
    return render(request, 'account/password_reset_confirm.html', {'validlink': False})
