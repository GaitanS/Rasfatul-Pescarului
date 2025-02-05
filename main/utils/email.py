from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger('django')

def send_email(to_email, subject, template, context=None):
    """
    Send an HTML email using a template
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        template (str): Path to HTML template
        context (dict): Template context variables
    """
    try:
        if context is None:
            context = {}
        
        # Add common context variables
        context.update({
            'site_url': settings.SITE_URL,
            'settings': settings,
            'logo_url': f"{settings.SITE_URL}/static/images/logo.png",
            'current_year': settings.CURRENT_YEAR
        })
        
        # Add order URL if order is in context
        if 'order' in context:
            order_url = reverse('main:order_detail', args=[context['order'].id])
            context['order_url'] = f"{settings.SITE_URL}{order_url}"
            
            # Add shipping address
            address_parts = [
                context['order'].full_name,
                context['order'].address,
                context['order'].city,
                context['order'].county.name if context['order'].county else '',
                context['order'].postal_code,
                f"Telefon: {context['order'].phone}",
                f"Email: {context['order'].email}"
            ]
            context['shipping_address'] = "\n".join(filter(None, address_parts))
            
            # Calculate total with shipping
            total = context['order'].total_amount
            context['order'].total_with_shipping = total if total >= 200 else total + 20
        
        # Render HTML content
        html_content = render_to_string(template, context)
        
        # Create plain text version
        text_content = strip_tags(html_content)
        
        # Create email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        
        # Attach HTML content
        msg.attach_alternative(html_content, "text/html")
        
        # Send email
        msg.send()
        logger.info(f'Email sent successfully to {to_email}: {subject}')
        
    except Exception as e:
        logger.error(f'Error sending email to {to_email}: {str(e)}')
        raise

def send_order_confirmation(order):
    """Send order confirmation email"""
    try:
        send_email(
            to_email=order.email,
            subject=f'Confirmare comandă #{order.id}',
            template='emails/order_confirmation.html',
            context={'order': order}
        )
    except Exception as e:
        logger.error(f'Error sending order confirmation email for order #{order.id}: {str(e)}')
        raise

def send_order_status_update(order):
    """Send order status update email"""
    try:
        template_map = {
            'shipped': 'emails/order_shipped.html',
            'delivered': 'emails/order_delivered.html',
            'cancelled': 'emails/order_cancelled.html',
        }
        
        template = template_map.get(order.status)
        if template:
            send_email(
                to_email=order.email,
                subject=f'Update comandă #{order.id}',
                template=template,
                context={'order': order}
            )
    except Exception as e:
        logger.error(f'Error sending order status update email for order #{order.id}: {str(e)}')
        raise