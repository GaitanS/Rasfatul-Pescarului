from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .models import Order, Payment
from .utils.email import send_email
import stripe
import logging

logger = logging.getLogger('django')
stripe.api_key = settings.STRIPE_SECRET_KEY

def check_pending_payments():
    """Check orders that have been in awaiting_payment status for more than 3 minutes"""
    threshold_time = timezone.now() - timedelta(minutes=3)
    pending_orders = Order.objects.filter(
        status='awaiting_payment',
        created_at__lte=threshold_time
    )

    for order in pending_orders:
        try:
            # Send reminder email
            retry_url = f"{settings.SITE_URL}{reverse('main:retry_payment', args=[order.id])}"
            send_email(
                to_email=order.email,
                subject=f'Finalizează plata pentru comanda #{order.id}',
                template='emails/payment_reminder.html',
                context={
                    'order': order,
                    'retry_url': retry_url
                }
            )
            logger.info(f'Sent payment reminder for order #{order.id}')

        except Exception as e:
            logger.error(f'Error sending payment reminder for order #{order.id}: {str(e)}')

def create_new_checkout_session(order):
    """Create a new Stripe checkout session for retrying payment"""
    try:
        # Create line items for Stripe
        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'ron',
                    'unit_amount': int(item.unit_price * 100),
                    'product_data': {
                        'name': item.product.name,
                        'description': item.product.description[:255] if item.product.description else None,
                    },
                },
                'quantity': item.quantity,
            })

        # Add shipping cost if applicable
        if order.shipping_cost > 0:
            line_items.append({
                'price_data': {
                    'currency': 'ron',
                    'unit_amount': int(order.shipping_cost * 100),
                    'product_data': {
                        'name': 'Transport',
                    },
                },
                'quantity': 1,
            })

        success_url = f"{settings.SITE_URL}{reverse('main:checkout_success')}"
        cancel_url = f"{settings.SITE_URL}{reverse('main:order_detail', args=[order.id])}"

        # Set expiration time to 30 minutes from now
        expires_at = int(timezone.now().timestamp()) + (30 * 60)

        # Create new checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_url,
            customer_email=order.email,
            client_reference_id=str(order.id),
            metadata={
                'order_id': str(order.id),
                'user_id': str(order.user.id),
                'retry_attempt': 'true'
            },
            payment_intent_data={
                'description': f'Comandă #{order.id} - {settings.COMPANY_NAME} (Reîncercare)',
                'metadata': {
                    'order_id': str(order.id),
                    'user_id': str(order.user.id),
                    'retry_attempt': 'true'
                },
            },
            expires_at=expires_at,
            locale='ro',
            allow_promotion_codes=True,
            billing_address_collection='required',
            shipping_address_collection={
                'allowed_countries': ['RO'],
            },
        )

        # Update order status
        order.status = 'awaiting_payment'
        order.save()

        return {
            'session_id': session.id,
            'checkout_url': session.url
        }

    except stripe.error.StripeError as e:
        logger.error(f'Error creating new checkout session for order #{order.id}: {str(e)}')
        return {
            'error': str(e)
        }

def get_payment_status(order):
    """Get detailed payment status for an order"""
    try:
        payments = Payment.objects.filter(order=order).order_by('-created_at')
        latest_payment = payments.first()

        if latest_payment and latest_payment.transaction_id:
            # Get payment intent details from Stripe
            payment_intent = stripe.PaymentIntent.retrieve(latest_payment.transaction_id)
            return {
                'status': payment_intent.status,
                'last_payment_error': payment_intent.last_payment_error.message if payment_intent.last_payment_error else None,
                'payment_method': payment_intent.payment_method_types[0] if payment_intent.payment_method_types else None,
                'amount': payment_intent.amount / 100,
                'created': timezone.datetime.fromtimestamp(payment_intent.created, tz=timezone.utc),
                'latest_attempt': latest_payment.created_at
            }
    except stripe.error.StripeError as e:
        logger.error(f'Error getting payment status for order #{order.id}: {str(e)}')
        return None

    return None