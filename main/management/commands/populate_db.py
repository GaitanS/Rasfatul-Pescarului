from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from main.models import (
    Category, Product, County, Lake, Video, Testimonial,
    Brand, ProductAttribute, ProductAttributeValue, ProductReview
)
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create brands
        brands = [
            {'name': 'Shimano', 'description': 'Lider mondial în echipamente de pescuit'},
            {'name': 'Daiwa', 'description': 'Calitate japoneză pentru pescari pretențioși'},
            {'name': 'Carp Expert', 'description': 'Specialiști în pescuitul la crap'},
            {'name': 'Maver', 'description': 'Echipamente premium pentru pescuit sportiv'},
            {'name': 'Trabucco', 'description': 'Tradiție și inovație în pescuit'}
        ]

        for brand_data in brands:
            brand, created = Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults={
                    'description': brand_data['description'],
                    'slug': slugify(brand_data['name'])
                }
            )
            self.stdout.write(f'Created brand: {brand.name}')

        # Create product attributes
        attributes = [
            {'name': 'Lungime', 'type': 'size', 'values': ['3.60m', '3.90m', '4.20m']},
            {'name': 'Putere lansare', 'type': 'weight', 'values': ['50-100g', '100-150g', '150-200g']},
            {'name': 'Culoare', 'type': 'color', 'values': ['Negru', 'Verde', 'Camuflaj']},
            {'name': 'Material', 'type': 'material', 'values': ['Carbon', 'Fibră de sticlă', 'Compozit']},
            {'name': 'Mărime', 'type': 'size', 'values': ['S', 'M', 'L', 'XL', 'XXL']}
        ]

        for attr_data in attributes:
            attr, created = ProductAttribute.objects.get_or_create(
                name=attr_data['name'],
                defaults={'type': attr_data['type'], 'is_filterable': True}
            )
            self.stdout.write(f'Created attribute: {attr.name}')

        # Create categories with parent-child relationships
        main_categories = [
            {
                'name': 'Lansete',
                'description': 'Lansete profesionale pentru pescuit',
                'subcategories': [
                    {'name': 'Lansete crap', 'description': 'Lansete specializate pentru crap'},
                    {'name': 'Lansete feeder', 'description': 'Lansete pentru pescuit la feeder'},
                    {'name': 'Lansete spinning', 'description': 'Lansete pentru pescuit la răpitor'}
                ]
            },
            {
                'name': 'Mulinete',
                'description': 'Mulinete de calitate superioară',
                'subcategories': [
                    {'name': 'Mulinete crap', 'description': 'Mulinete pentru pescuit la crap'},
                    {'name': 'Mulinete feeder', 'description': 'Mulinete pentru pescuit la feeder'},
                    {'name': 'Mulinete spinning', 'description': 'Mulinete pentru pescuit la răpitor'}
                ]
            }
        ]

        for cat_data in main_categories:
            parent, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': slugify(cat_data['name'])
                }
            )
            self.stdout.write(f'Created parent category: {parent.name}')

            for subcat_data in cat_data['subcategories']:
                child, created = Category.objects.get_or_create(
                    name=subcat_data['name'],
                    defaults={
                        'description': subcat_data['description'],
                        'parent': parent,
                        'slug': slugify(subcat_data['name'])
                    }
                )
                self.stdout.write(f'Created child category: {child.name}')

        # Create products with attributes and reviews
        products = [
            {
                'name': 'Lansetă Carbon Pro',
                'category': 'Lansete crap',
                'brand': 'Shimano',
                'description': 'Lansetă profesională din carbon',
                'price': Decimal('299.99'),
                'stock_quantity': 10,
                'is_featured': True,
                'attributes': {
                    'Lungime': '3.90m',
                    'Putere lansare': '100-150g',
                    'Culoare': 'Negru',
                    'Material': 'Carbon'
                }
            },
            {
                'name': 'Mulinetă Big Pit',
                'category': 'Mulinete crap',
                'brand': 'Daiwa',
                'description': 'Mulinetă de înaltă performanță',
                'price': Decimal('449.99'),
                'stock_quantity': 5,
                'is_featured': True,
                'attributes': {
                    'Culoare': 'Negru',
                    'Material': 'Carbon'
                }
            }
        ]

        # Create a test user for reviews
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('test123')
            user.save()

        for prod_data in products:
            category = Category.objects.get(name=prod_data['category'])
            brand = Brand.objects.get(name=prod_data['brand'])
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'brand': brand,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock_quantity': prod_data['stock_quantity'],
                    'is_featured': prod_data['is_featured'],
                    'slug': slugify(prod_data['name'])
                }
            )

            # Add attributes
            for attr_name, value in prod_data['attributes'].items():
                attribute = ProductAttribute.objects.get(name=attr_name)
                ProductAttributeValue.objects.get_or_create(
                    product=product,
                    attribute=attribute,
                    defaults={'value': value}
                )

            # Add reviews
            for i in range(3):
                review, created = ProductReview.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'rating': random.randint(4, 5),
                        'comment': f'Review {i+1} pentru {product.name}',
                        'is_approved': True
                    }
                )

            self.stdout.write(f'Created product with attributes and reviews: {product.name}')

        # Create counties and lakes (existing code)
        counties = [
            {'name': 'București', 'region': 'București-Ilfov'},
            {'name': 'Ilfov', 'region': 'București-Ilfov'},
            {'name': 'Cluj', 'region': 'Transilvania'}
        ]

        for county_data in counties:
            county, created = County.objects.get_or_create(
                name=county_data['name'],
                defaults={
                    'region': county_data['region'],
                    'slug': slugify(county_data['name'])
                }
            )
            self.stdout.write(f'Created county: {county.name}')

        lakes = [
            {
                'name': 'Lacul Morii',
                'county': 'București',
                'description': 'Lac de acumulare perfect pentru pescuit de crap',
                'address': 'Sector 6, București',
                'latitude': Decimal('44.4478'),
                'longitude': Decimal('26.0167'),
                'fish_types': 'crap,caras,șalău',
                'facilities': 'parcare,toalete,chioșc',
                'rules': 'Pescuitul permis între orele 6:00-22:00',
                'price_per_day': Decimal('50.00')
            }
        ]

        for lake_data in lakes:
            county = County.objects.get(name=lake_data['county'])
            lake, created = Lake.objects.get_or_create(
                name=lake_data['name'],
                defaults={
                    'county': county,
                    'description': lake_data['description'],
                    'address': lake_data['address'],
                    'latitude': lake_data['latitude'],
                    'longitude': lake_data['longitude'],
                    'fish_types': lake_data['fish_types'],
                    'facilities': lake_data['facilities'],
                    'rules': lake_data['rules'],
                    'price_per_day': lake_data['price_per_day']
                }
            )
            self.stdout.write(f'Created lake: {lake.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
