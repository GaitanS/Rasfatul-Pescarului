from django.core.management.base import BaseCommand
from main.tasks import check_pending_payments

class Command(BaseCommand):
    help = 'Check orders with pending payments and send reminders'

    def handle(self, *args, **kwargs):
        try:
            check_pending_payments()
            self.stdout.write(self.style.SUCCESS('Successfully checked pending payments'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error checking pending payments: {str(e)}'))