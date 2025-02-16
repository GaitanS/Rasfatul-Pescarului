from django.core.management.base import BaseCommand
from main.models import Lake, County

class Command(BaseCommand):
    help = 'Creates test data for lakes and counties'

    def handle(self, *args, **kwargs):
        # Create counties
        counties = [
            {'name': 'Argeș', 'slug': 'arges', 'region': 'Muntenia'},
            {'name': 'Giurgiu', 'slug': 'giurgiu', 'region': 'Muntenia'},
            {'name': 'Ilfov', 'slug': 'ilfov', 'region': 'Muntenia'},
        ]

        for county_data in counties:
            county, created = County.objects.get_or_create(
                slug=county_data['slug'],
                defaults={
                    'name': county_data['name'],
                    'region': county_data['region']
                }
            )
            if created:
                self.stdout.write(f'Created county: {county.name}')

        # Create lakes
        lakes = [
            {
                'name': 'Balta Căldărușani',
                'county_slug': 'ilfov',
                'description': 'Lac natural cu o suprafață de peste 200 hectare, bogat în crap, caras și șalău.',
                'address': 'Comuna Gruiu, Județul Ilfov',
                'latitude': 44.7167,
                'longitude': 26.2667,
                'fish_types': 'Crap, Caras, Șalău',
                'facilities': 'parcare cazare restaurant toalete',
                'rules': 'Pescuitul este permis doar cu permis. Camparea este permisă în zonele desemnate.',
                'price_per_day': 50.00,
                'is_active': True
            },
            {
                'name': 'Balta Comana',
                'county_slug': 'giurgiu',
                'description': 'Complex de lacuri în Parcul Natural Comana, perfect pentru pescuitul sportiv.',
                'address': 'Comuna Comana, Județul Giurgiu',
                'latitude': 44.1833,
                'longitude': 26.1500,
                'fish_types': 'Crap, Caras, Știucă',
                'facilities': 'parcare restaurant toalete',
                'rules': 'Pescuit catch & release recomandat. Nu este permis pescuitul noaptea.',
                'price_per_day': 40.00,
                'is_active': True
            },
            {
                'name': 'Balta Budeasa',
                'county_slug': 'arges',
                'description': 'Lac de acumulare pe râul Argeș, cunoscut pentru pescuitul la crap și șalău.',
                'address': 'Comuna Budeasa, Județul Argeș',
                'latitude': 44.9500,
                'longitude': 24.8667,
                'fish_types': 'Crap, Șalău, Știucă',
                'facilities': 'parcare cazare toalete',
                'rules': 'Se permite pescuitul din barcă. Este necesară rezervare în avans.',
                'price_per_day': 60.00,
                'is_active': True
            }
        ]

        for lake_data in lakes:
            county = County.objects.get(slug=lake_data.pop('county_slug'))
            lake, created = Lake.objects.get_or_create(
                name=lake_data['name'],
                county=county,
                defaults=lake_data
            )
            if created:
                self.stdout.write(f'Created lake: {lake.name}')
