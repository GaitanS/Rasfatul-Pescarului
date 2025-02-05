import stripe
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
import time

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentProcessor:
    @staticmethod
    def create_checkout_session(request, order):
        """
        Create a Stripe Checkout Session for an order
        """
        try:
            success_url = request.build_absolute_uri(reverse('main:checkout_success'))
            cancel_url = request.build_absolute_uri(reverse('main:checkout'))

            # Create line items for Stripe
            line_items = []
            for item in order.items.all():
                line_items.append({
                    'price_data': {
                        'currency': 'ron',
                        'unit_amount': int(item.unit_price * 100),  # Convert to cents
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

            # Set expiration time to 30 minutes from now
            expires_at = int(time.time()) + (30 * 60)

            # Create checkout session
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
                },
                payment_intent_data={
                    'description': f'Comandă #{order.id} - {settings.COMPANY_NAME}',
                    'metadata': {
                        'order_id': str(order.id),
                        'user_id': str(order.user.id),
                    },
                },
                expires_at=expires_at,  # Session expires in 30 minutes
                locale='ro',
                allow_promotion_codes=True,
                billing_address_collection='required',
                shipping_address_collection={
                    'allowed_countries': ['RO'],
                },
            )

            # Update order status to awaiting_payment
            order.status = 'awaiting_payment'
            order.save()

            return {
                'session_id': session.id,
                'checkout_url': session.url,
            }

        except stripe.error.StripeError as e:
            # If there's an error, mark the order as payment_failed
            order.status = 'payment_failed'
            order.save()
            return {
                'error': str(e)
            }

    @staticmethod
    def handle_webhook(request):
        """
        Handle Stripe webhook events
        """
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        from main.models import Order, Payment

        if event.type == 'checkout.session.completed':
            session = event.data.object
            order_id = session.metadata.get('order_id')
            
            try:
                order = Order.objects.get(id=order_id)
                # Create payment record
                Payment.objects.create(
                    order=order,
                    payment_method='card',
                    transaction_id=session.payment_intent,
                    amount=session.amount_total / 100,  # Convert from cents
                    status='completed'
                )
                # Update order status
                order.status = 'paid'
                order.save()
                
                # Send confirmation email
                from .email import send_order_confirmation
                send_order_confirmation(order)
                
            except Order.DoesNotExist:
                return HttpResponse(status=404)

        elif event.type in ['charge.failed', 'payment_intent.payment_failed']:
            payment_data = event.data.object
            order_id = payment_data.metadata.get('order_id')
            
            try:
                order = Order.objects.get(id=order_id)
                # Create failed payment record
                Payment.objects.create(
                    order=order,
                    payment_method='card',
                    transaction_id=payment_data.id,
                    amount=payment_data.amount / 100,
                    status='failed'
                )
                # Update order status
                order.status = 'payment_failed'
                order.save()
                
            except Order.DoesNotExist:
                return HttpResponse(status=404)

        elif event.type == 'checkout.session.expired':
            session = event.data.object
            order_id = session.metadata.get('order_id')
            
            try:
                order = Order.objects.get(id=order_id)
                if order.status == 'awaiting_payment':
                    order.status = 'payment_failed'
                    order.save()
            except Order.DoesNotExist:
                return HttpResponse(status=404)

        return HttpResponse(status=200)
