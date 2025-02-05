from django.core.management.base import BaseCommand
from main.models import County, Lake
from decimal import Decimal
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create counties and lakes'

    def handle(self, *args, **kwargs):
        # Create counties with their regions
        counties_data = {
            'Alba': 'Transilvania',
            'Arad': 'Crișana',
            'Argeș': 'Muntenia',
            'Bacău': 'Moldova',
            'Bihor': 'Crișana',
            'Bistrița-Năsăud': 'Transilvania',
            'Botoșani': 'Moldova',
            'Brăila': 'Muntenia',
            'Brașov': 'Transilvania',
            'București': 'Muntenia',
            'Buzău': 'Muntenia',
            'Călărași': 'Muntenia',
            'Caraș-Severin': 'Banat',
            'Cluj': 'Transilvania',
            'Constanța': 'Dobrogea',
            'Covasna': 'Transilvania',
            'Dâmbovița': 'Muntenia',
            'Dolj': 'Oltenia',
            'Galați': 'Moldova',
            'Giurgiu': 'Muntenia',
            'Gorj': 'Oltenia',
            'Harghita': 'Transilvania',
            'Hunedoara': 'Transilvania',
            'Ialomița': 'Muntenia',
            'Iași': 'Moldova',
            'Ilfov': 'Muntenia',
            'Maramureș': 'Transilvania',
            'Mehedinți': 'Oltenia',
            'Mureș': 'Transilvania',
            'Neamț': 'Moldova',
            'Olt': 'Oltenia',
            'Prahova': 'Muntenia',
            'Sălaj': 'Transilvania',
            'Satu Mare': 'Transilvania',
            'Sibiu': 'Transilvania',
            'Suceava': 'Moldova',
            'Teleorman': 'Muntenia',
            'Timiș': 'Banat',
            'Tulcea': 'Dobrogea',
            'Vâlcea': 'Oltenia',
            'Vaslui': 'Moldova',
            'Vrancea': 'Moldova'
        }

        for name, region in counties_data.items():
            county, created = County.objects.get_or_create(
                name=name,
                defaults={
                    'region': region,
                    'created_at': timezone.now()
                }
            )
            if created:
                self.stdout.write(f'Created county: {county.name} ({region})')

        # Create lakes with real coordinates
        lakes = [
            {
                'name': 'Balta Corbu',
                'county': 'Constanța',
                'description': 'Complex de bălți amenajate pentru pescuit sportiv, cu o suprafață totală de peste 100 hectare. Specii de pești: crap, caras, șalău, știucă.',
                'location': 'Comuna Corbu, Constanța',
                'latitude': Decimal('44.3778'),
                'longitude': Decimal('28.6447')
            },
            {
                'name': 'Lacul Morii',
                'county': 'București',
                'description': 'Cel mai mare lac din București, perfect pentru pescuit de crap și caras. Facilități: pontoane, parcare, chioșc.',
                'location': 'Sector 6, București',
                'latitude': Decimal('44.4478'),
                'longitude': Decimal('26.0167')
            },
            {
                'name': 'Balta Căldărușani',
                'county': 'Ilfov',
                'description': 'Lac natural cu o suprafață de 224 hectare, bogat în pește și cu facilități moderne. Specii: crap, caras, șalău, somn.',
                'location': 'Comuna Gruiu, Ilfov',
                'latitude': Decimal('44.6833'),
                'longitude': Decimal('26.2667')
            },
            {
                'name': 'Lacul Snagov',
                'county': 'Ilfov',
                'description': 'Unul dintre cele mai cunoscute lacuri pentru pescuit din România. Facilități complete și specii variate de pești.',
                'location': 'Snagov, Ilfov',
                'latitude': Decimal('44.7000'),
                'longitude': Decimal('26.1667')
            },
            {
                'name': 'Balta Comana',
                'county': 'Giurgiu',
                'description': 'Complex piscicol situat în Parcul Natural Comana. Pescuit sportiv și de agrement într-un cadru natural deosebit.',
                'location': 'Comuna Comana, Giurgiu',
                'latitude': Decimal('44.1667'),
                'longitude': Decimal('26.1500')
            },
            {
                'name': 'Lacul Vidraru',
                'county': 'Argeș',
                'description': 'Lac de acumulare situat pe râul Argeș, perfect pentru pescuit de păstrăv. Peisaj montan spectaculos.',
                'location': 'Arefu, Argeș',
                'latitude': Decimal('45.3667'),
                'longitude': Decimal('24.6333')
            },
            {
                'name': 'Balta Zătun',
                'county': 'Galați',
                'description': 'Complex de bălți amenajat pentru pescuit sportiv. Specii predominante: crap, caras, șalău. Facilități complete.',
                'location': 'Comuna Schela, Galați',
                'latitude': Decimal('45.3833'),
                'longitude': Decimal('28.0333')
            },
            {
                'name': 'Lacul Bicaz',
                'county': 'Neamț',
                'description': 'Cel mai mare lac de acumulare din România, bogat în clean și șalău. Pescuit la răpitori și ciprinide.',
                'location': 'Bicaz, Neamț',
                'latitude': Decimal('46.9333'),
                'longitude': Decimal('26.1000')
            },
            {
                'name': 'Balta Putineiu',
                'county': 'Giurgiu',
                'description': 'Complex piscicol format din mai multe bălți, ideal pentru pescuit de crap. Facilități moderne și cazare.',
                'location': 'Comuna Putineiu, Giurgiu',
                'latitude': Decimal('43.9667'),
                'longitude': Decimal('25.6333')
            },
            {
                'name': 'Lacul Fântânele',
                'county': 'Cluj',
                'description': 'Lac de acumulare situat pe Someșul Cald, bogat în păstrăv și clean. Pescuit montan în peisaj spectaculos.',
                'location': 'Comuna Beliș, Cluj',
                'latitude': Decimal('46.6333'),
                'longitude': Decimal('23.0167')
            }
        ]

        # Create lakes
        for lake_data in lakes:
            county = County.objects.get(name=lake_data['county'])
            lake, created = Lake.objects.get_or_create(
                name=lake_data['name'],
                defaults={
                    'county': county,
                    'description': lake_data['description'],
                    'location': lake_data['location'],
                    'latitude': lake_data['latitude'],
                    'longitude': lake_data['longitude'],
                    'is_active': True,
                    'created_at': timezone.now()
                }
            )
            if created:
                self.stdout.write(f'Created lake: {lake.name} in {lake.county.name}')
