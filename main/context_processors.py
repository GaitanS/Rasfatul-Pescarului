from django.shortcuts import get_object_or_404
from .models import Product
from django.conf import settings
import logging
import json
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)

def debug_session(request, message=""):
    """Debug helper to log session information"""
    logger.debug(f"=== Context Processor Session Debug: {message} ===")
    logger.debug(f"Session ID: {request.session.session_key}")
    logger.debug(f"Session Modified: {request.session.modified}")
    logger.debug(f"Session Data: {dict(request.session)}")
    logger.debug(f"Session Cookie Age: {settings.SESSION_COOKIE_AGE}")
    logger.debug(f"Session Save Every Request: {settings.SESSION_SAVE_EVERY_REQUEST}")
    logger.debug("=" * 50)

def cart_processor(request):
    """Add cart information to all templates"""
    try:
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()
            logger.debug(f'Created new session: {request.session.session_key}')

        debug_session(request, "Cart processor start")

        # Initialize cart if it doesn't exist
        if 'cart' not in request.session:
            logger.debug('Initializing new cart in session')
            request.session['cart'] = {}
            request.session.modified = True
            request.session.save()

        cart = request.session.get('cart', {})
        cart_items = []
        total = Decimal('0.00')
        items_count = 0

        logger.debug(f'Processing cart for session {request.session.session_key}')
        logger.debug(f'Raw cart data: {json.dumps(cart)}')
        
        # Calculate cart totals
        for product_id, item_data in cart.items():
            try:
                product = get_object_or_404(Product, id=int(product_id))
                quantity = int(item_data['quantity'])
                item_total = Decimal(str(product.price)) * quantity
                item_total = item_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                total += item_total
                items_count += quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': item_total
                })
                logger.debug(f'Added product {product_id} to cart context: {quantity} x {product.price} = {item_total}')
            except Product.DoesNotExist:
                logger.warning(f'Product {product_id} not found in database, removing from cart')
                del cart[product_id]
                request.session.modified = True
                request.session.save()
                continue
            except (ValueError, TypeError) as e:
                logger.error(f'Error calculating cart item total: {str(e)}')
                continue

        # Calculate shipping and total
        shipping_cost = Decimal('20.00') if total < Decimal('200.00') else Decimal('0.00')
        total_with_shipping = (total + shipping_cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        free_shipping_remaining = max(Decimal('0.00'), Decimal('200.00') - total)
        free_shipping_remaining = free_shipping_remaining.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        logger.debug(f'Cart summary - Items: {items_count}, Total: {total}, Shipping: {shipping_cost}')

        # Force session save
        request.session.modified = True
        request.session.save()

        debug_session(request, "Cart processor end")
        
        return {
            'cart_items': cart_items,
            'cart_count': items_count,
            'cart_total': total,
            'shipping_cost': shipping_cost,
            'total_with_shipping': total_with_shipping,
            'free_shipping_remaining': free_shipping_remaining,
            'cart_empty': items_count == 0,
            'cart': cart,  # Include raw cart data for debugging
            'debug': settings.DEBUG,  # For cart.js debug mode
            'session_id': request.session.session_key,  # For cart.js session tracking
            'debug_info': {
                'session_key': request.session.session_key,
                'session_modified': request.session.modified,
                'cart_data': cart,
                'items_count': items_count,
                'total': total,
                'shipping_cost': shipping_cost
            } if settings.DEBUG else None
        }
    except Exception as e:
        logger.error(f'Error in cart_processor: {str(e)}', exc_info=True)
        # If any error occurs, return empty cart
        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True
            request.session.save()
        return {
            'cart_items': [],
            'cart_count': 0,
            'cart_total': Decimal('0.00'),
            'shipping_cost': Decimal('20.00'),
            'total_with_shipping': Decimal('0.00'),
            'free_shipping_remaining': Decimal('200.00'),
            'cart_empty': True,
            'cart': {},
            'debug': settings.DEBUG,
            'session_id': request.session.session_key if hasattr(request, 'session') else None,
            'debug_info': {
                'error': str(e),
                'session_key': request.session.session_key if hasattr(request, 'session') else None,
                'session_modified': request.session.modified if hasattr(request, 'session') else None
            } if settings.DEBUG else None
        }
