from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Category, Product, County, Lake, Video, Testimonial
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories = [
            {
                'name': 'Lansete',
                'description': 'Lansete profesionale pentru pescuit'
            },
            {
                'name': 'Mulinete',
                'description': 'Mulinete de calitate superioară'
            },
            {
                'name': 'Momeli',
                'description': 'Momeli naturale și artificiale'
            },
            {
                'name': 'Accesorii',
                'description': 'Accesorii pentru pescuit'
            },
            {
                'name': 'Îmbrăcăminte',
                'description': 'Îmbrăcăminte pentru pescuit'
            },
            {
                'name': 'Echipament camping',
                'description': 'Echipament pentru camping'
            }
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            self.stdout.write(f'Created category: {category.name}')

        # Create products
        products = [
            {
                'name': 'Lansetă Carbon Pro',
                'category': 'Lansete',
                'description': 'Lansetă profesională din carbon',
                'price': Decimal('299.99'),
                'stock_quantity': 10,
                'is_featured': True
            },
            {
                'name': 'Mulinetă Shimano XT',
                'category': 'Mulinete',
                'description': 'Mulinetă de înaltă calitate',
                'price': Decimal('449.99'),
                'stock_quantity': 5,
                'is_featured': True
            },
            {
                'name': 'Set momeli artificiale',
                'category': 'Momeli',
                'description': 'Set de 10 momeli artificiale',
                'price': Decimal('99.99'),
                'stock_quantity': 20,
                'is_featured': False
            },
            {
                'name': 'Cort 2 persoane',
                'category': 'Echipament camping',
                'description': 'Cort impermeabil, perfect pentru sesiuni lungi de pescuit',
                'price': Decimal('399.99'),
                'stock_quantity': 8,
                'is_featured': True
            },
            {
                'name': 'Scaun pescar deluxe',
                'category': 'Accesorii',
                'description': 'Scaun confortabil cu suport pentru băutură și undiță',
                'price': Decimal('199.99'),
                'stock_quantity': 15,
                'is_featured': True
            },
            {
                'name': 'Geacă impermeabilă',
                'category': 'Îmbrăcăminte',
                'description': 'Geacă impermeabilă și călduroasă pentru pescuit în orice sezon',
                'price': Decimal('249.99'),
                'stock_quantity': 12,
                'is_featured': False
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
                    'is_featured': prod_data['is_featured']
                }
            )
            self.stdout.write(f'Created product: {product.name}')

        # Create counties
        counties = [
            {'name': 'Alba', 'region': 'Transilvania'},
            {'name': 'Arad', 'region': 'Crișana'},
            {'name': 'Argeș', 'region': 'Muntenia'},
            {'name': 'Bacău', 'region': 'Moldova'},
            {'name': 'Bihor', 'region': 'Crișana'},
            {'name': 'Bistrița-Năsăud', 'region': 'Transilvania'},
            {'name': 'Botoșani', 'region': 'Moldova'},
            {'name': 'Brăila', 'region': 'Muntenia'},
            {'name': 'Brașov', 'region': 'Transilvania'},
            {'name': 'București', 'region': 'București-Ilfov'},
            {'name': 'Buzău', 'region': 'Muntenia'},
            {'name': 'Călărași', 'region': 'Muntenia'},
            {'name': 'Caraș-Severin', 'region': 'Banat'},
            {'name': 'Cluj', 'region': 'Transilvania'},
            {'name': 'Constanța', 'region': 'Dobrogea'},
            {'name': 'Covasna', 'region': 'Transilvania'},
            {'name': 'Dâmbovița', 'region': 'Muntenia'},
            {'name': 'Dolj', 'region': 'Oltenia'},
            {'name': 'Galați', 'region': 'Moldova'},
            {'name': 'Giurgiu', 'region': 'Muntenia'},
            {'name': 'Gorj', 'region': 'Oltenia'},
            {'name': 'Harghita', 'region': 'Transilvania'},
            {'name': 'Hunedoara', 'region': 'Transilvania'},
            {'name': 'Ialomița', 'region': 'Muntenia'},
            {'name': 'Iași', 'region': 'Moldova'},
            {'name': 'Ilfov', 'region': 'București-Ilfov'},
            {'name': 'Maramureș', 'region': 'Transilvania'},
            {'name': 'Mehedinți', 'region': 'Oltenia'},
            {'name': 'Mureș', 'region': 'Transilvania'},
            {'name': 'Neamț', 'region': 'Moldova'},
            {'name': 'Olt', 'region': 'Oltenia'},
            {'name': 'Prahova', 'region': 'Muntenia'},
            {'name': 'Sălaj', 'region': 'Transilvania'},
            {'name': 'Satu Mare', 'region': 'Transilvania'},
            {'name': 'Sibiu', 'region': 'Transilvania'},
            {'name': 'Suceava', 'region': 'Moldova'},
            {'name': 'Teleorman', 'region': 'Muntenia'},
            {'name': 'Timiș', 'region': 'Banat'},
            {'name': 'Tulcea', 'region': 'Dobrogea'},
            {'name': 'Vâlcea', 'region': 'Oltenia'},
            {'name': 'Vaslui', 'region': 'Moldova'},
            {'name': 'Vrancea', 'region': 'Moldova'}
        ]

        for county_data in counties:
            county, created = County.objects.get_or_create(
                name=county_data['name'],
                defaults={'region': county_data['region']}
            )
            self.stdout.write(f'Created county: {county.name}')

        # Create lakes
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
            },
            {
                'name': 'Balta Corbu',
                'county': 'Constanța',
                'description': 'Complex de bălți amenajate pentru pescuit sportiv',
                'address': 'Comuna Corbu, Constanța',
                'latitude': Decimal('44.3778'),
                'longitude': Decimal('28.6447'),
                'fish_types': 'crap,caras,știucă',
                'facilities': 'parcare,cazare,restaurant',
                'rules': 'Pescuit catch & release obligatoriu',
                'price_per_day': Decimal('80.00')
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

        # Create videos
        videos = [
            {
                'title': 'Tehnici de pescuit la crap',
                'category': 'Lansete',
                'description': 'Învață cele mai eficiente tehnici de pescuit la crap',
                'embed_url': 'https://www.youtube.com/embed/abc123',
                'is_featured': True
            },
            {
                'title': 'Cum să alegi mulineta potrivită',
                'category': 'Mulinete',
                'description': 'Ghid complet pentru alegerea mulinetei perfecte',
                'embed_url': 'https://www.youtube.com/embed/def456',
                'is_featured': True
            },
            {
                'title': 'Pescuit la răpitor',
                'category': 'Momeli',
                'description': 'Sfaturi pentru pescuitul la știucă și șalău',
                'embed_url': 'https://www.youtube.com/embed/ghi789',
                'is_featured': True
            }
        ]

        for video_data in videos:
            category = Category.objects.get(name=video_data['category'])
            video, created = Video.objects.get_or_create(
                title=video_data['title'],
                defaults={
                    'category': category,
                    'description': video_data['description'],
                    'embed_url': video_data['embed_url'],
                    'is_featured': video_data['is_featured']
                }
            )
            self.stdout.write(f'Created video: {video.title}')

        # Create testimonials
        testimonials = [
            {
                'name': 'Ioan Popescu',
                'content': 'Cel mai bun magazin de pescuit! Produse de calitate și livrare rapidă.',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'Andrei Popa',
                'content': 'Recomand cu încredere! Echipa foarte amabilă și profesionistă.',
                'rating': 5,
                'is_active': True
            },
            {
                'name': 'Maria Ionescu',
                'content': 'Am găsit tot ce aveam nevoie pentru pescuit. Prețuri foarte bune!',
                'rating': 4,
                'is_active': True
            }
        ]

        for testimonial_data in testimonials:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                defaults={
                    'content': testimonial_data['content'],
                    'rating': testimonial_data['rating'],
                    'is_active': testimonial_data['is_active']
                }
            )
            self.stdout.write(f'Created testimonial by: {testimonial.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
