from django.core.management.base import BaseCommand
from main.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create fishing products'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = {
            'lansete': {
                'name': 'Lansete',
                'description': 'Lansete profesionale pentru pescuit'
            },
            'mulinete': {
                'name': 'Mulinete',
                'description': 'Mulinete de calitate superioară'
            },
            'momeli': {
                'name': 'Momeli',
                'description': 'Momeli naturale și artificiale'
            }
        }

        for key, cat_data in categories.items():
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            self.stdout.write(f'Created category: {category.name}')

        # Create products
        products = [
            {
                'name': 'Lansetă Carbon Pro 3.6m',
                'category': 'Lansete',
                'description': 'Lansetă profesională din carbon, lungime 3.6m, putere de aruncare 60-120g',
                'price': Decimal('299.99'),
                'stock_quantity': 10
            },
            {
                'name': 'Lansetă Feeder 3.3m',
                'category': 'Lansete',
                'description': 'Lansetă feeder pentru pescuit la crap, lungime 3.3m, putere de aruncare 40-120g',
                'price': Decimal('249.99'),
                'stock_quantity': 15
            },
            {
                'name': 'Mulinetă Shimano Stradic FL 4000',
                'category': 'Mulinete',
                'description': 'Mulinetă de înaltă calitate cu 6+1 rulmenți, raport de recuperare 6.2:1',
                'price': Decimal('899.99'),
                'stock_quantity': 5
            },
            {
                'name': 'Mulinetă Daiwa Ninja 2500',
                'category': 'Mulinete',
                'description': 'Mulinetă fiabilă cu 4 rulmenți, sistem anti-răsucire și frână frontală',
                'price': Decimal('299.99'),
                'stock_quantity': 8
            },
            {
                'name': 'Set Momeli Artificiale Rapitori',
                'category': 'Momeli',
                'description': 'Set de 10 momeli artificiale pentru știucă și șalău, diverse culori',
                'price': Decimal('149.99'),
                'stock_quantity': 20
            },
            {
                'name': 'Lansetă Spinning 2.7m',
                'category': 'Lansete',
                'description': 'Lansetă spinning pentru răpitori, lungime 2.7m, putere de aruncare 10-30g',
                'price': Decimal('199.99'),
                'stock_quantity': 12
            },
            {
                'name': 'Mulinetă Okuma Ceymar 2500',
                'category': 'Mulinete',
                'description': 'Mulinetă ușoară cu 8 rulmenți, perfectă pentru spinning',
                'price': Decimal('249.99'),
                'stock_quantity': 7
            },
            {
                'name': 'Set Momeli Boilies Crap',
                'category': 'Momeli',
                'description': 'Set boilies pentru crap, diverse arome, 1kg',
                'price': Decimal('79.99'),
                'stock_quantity': 25
            },
            {
                'name': 'Lansetă Telescopică 5m',
                'category': 'Lansete',
                'description': 'Lansetă telescopică pentru pescuit la plută, lungime 5m',
                'price': Decimal('159.99'),
                'stock_quantity': 15
            },
            {
                'name': 'Set Momeli Method Feeder',
                'category': 'Momeli',
                'description': 'Set complet method feeder cu pelete și năduri, 2kg',
                'price': Decimal('89.99'),
                'stock_quantity': 18
            }
        ]

        for prod_data in products:
            category = Category.objects.get(name=prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock_quantity': prod_data['stock_quantity'],
                    'is_active': True
                }
            )
            self.stdout.write(f'Created product: {product.name}')
