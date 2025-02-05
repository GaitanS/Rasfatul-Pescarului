from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Order, Profile
from .utils.email import send_order_confirmation, send_order_status_update

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile instance when a new User is created"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    """Handle post-save actions for orders"""
    if created:
        # Send order confirmation email
        send_order_confirmation(instance)
    else:
        # Send order status update email
        send_order_status_update(instance)
