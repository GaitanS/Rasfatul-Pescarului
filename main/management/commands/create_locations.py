from django.core.management.base import BaseCommand
from main.models import Lake, County

class Command(BaseCommand):
    help = 'Creates counties and lakes data'

    def handle(self, *args, **kwargs):
        # Create counties organized by regions
        counties = [
            # Moldova
            {'name': 'Bacău', 'slug': 'bacau', 'region': 'Moldova'},
            {'name': 'Botoșani', 'slug': 'botosani', 'region': 'Moldova'},
            {'name': 'Iași', 'slug': 'iasi', 'region': 'Moldova'},
            {'name': 'Neamț', 'slug': 'neamt', 'region': 'Moldova'},
            {'name': 'Suceava', 'slug': 'suceava', 'region': 'Moldova'},
            {'name': 'Vaslui', 'slug': 'vaslui', 'region': 'Moldova'},
            {'name': 'Galați', 'slug': 'galati', 'region': 'Moldova'},
            {'name': 'Vrancea', 'slug': 'vrancea', 'region': 'Moldova'},

            # Muntenia
            {'name': 'Argeș', 'slug': 'arges', 'region': 'Muntenia'},
            {'name': 'Brăila', 'slug': 'braila', 'region': 'Muntenia'},
            {'name': 'Buzău', 'slug': 'buzau', 'region': 'Muntenia'},
            {'name': 'Dâmbovița', 'slug': 'dambovita', 'region': 'Muntenia'},
            {'name': 'Giurgiu', 'slug': 'giurgiu', 'region': 'Muntenia'},
            {'name': 'Ialomița', 'slug': 'ialomita', 'region': 'Muntenia'},
            {'name': 'Ilfov', 'slug': 'ilfov', 'region': 'Muntenia'},
            {'name': 'Prahova', 'slug': 'prahova', 'region': 'Muntenia'},
            {'name': 'Teleorman', 'slug': 'teleorman', 'region': 'Muntenia'},
            {'name': 'Călărași', 'slug': 'calarasi', 'region': 'Muntenia'},

            # Transilvania
            {'name': 'Alba', 'slug': 'alba', 'region': 'Transilvania'},
            {'name': 'Bistrița-Năsăud', 'slug': 'bistrita-nasaud', 'region': 'Transilvania'},
            {'name': 'Brașov', 'slug': 'brasov', 'region': 'Transilvania'},
            {'name': 'Cluj', 'slug': 'cluj', 'region': 'Transilvania'},
            {'name': 'Covasna', 'slug': 'covasna', 'region': 'Transilvania'},
            {'name': 'Harghita', 'slug': 'harghita', 'region': 'Transilvania'},
            {'name': 'Hunedoara', 'slug': 'hunedoara', 'region': 'Transilvania'},
            {'name': 'Mureș', 'slug': 'mures', 'region': 'Transilvania'},
            {'name': 'Sibiu', 'slug': 'sibiu', 'region': 'Transilvania'},
            {'name': 'Sălaj', 'slug': 'salaj', 'region': 'Transilvania'},

            # Banat
            {'name': 'Arad', 'slug': 'arad', 'region': 'Banat'},
            {'name': 'Caraș-Severin', 'slug': 'caras-severin', 'region': 'Banat'},
            {'name': 'Timiș', 'slug': 'timis', 'region': 'Banat'},

            # Crișana
            {'name': 'Bihor', 'slug': 'bihor', 'region': 'Crisana'},
            {'name': 'Satu Mare', 'slug': 'satu-mare', 'region': 'Crisana'},

            # Dobrogea
            {'name': 'Constanța', 'slug': 'constanta', 'region': 'Dobrogea'},
            {'name': 'Tulcea', 'slug': 'tulcea', 'region': 'Dobrogea'},

            # Oltenia
            {'name': 'Dolj', 'slug': 'dolj', 'region': 'Oltenia'},
            {'name': 'Gorj', 'slug': 'gorj', 'region': 'Oltenia'},
            {'name': 'Mehedinți', 'slug': 'mehedinti', 'region': 'Oltenia'},
            {'name': 'Olt', 'slug': 'olt', 'region': 'Oltenia'},
            {'name': 'Vâlcea', 'slug': 'valcea', 'region': 'Oltenia'},
        ]

        # Create counties
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
            # Moldova
            {
                'name': 'Lacul Bicaz',
                'county_slug': 'neamt',
                'description': 'Cel mai mare lac de acumulare din România, cu o suprafață de peste 3.000 hectare.',
                'address': 'Comuna Bicaz-Chei, Județul Neamț',
                'latitude': 46.9283,
                'longitude': 26.1024,
                'fish_types': 'Crap, Șalău, Știucă, Clean, Biban',
                'facilities': 'parcare cazare restaurant toalete',
                'rules': 'Permis obligatoriu. Se permite pescuitul din barcă.',
                'price_per_day': 50.00,
                'is_active': True
            },
            {
                'name': 'Lacul Ciric',
                'county_slug': 'iasi',
                'description': 'Complex de agrement cu trei lacuri pentru pescuit sportiv.',
                'address': 'Iași, Județul Iași',
                'latitude': 47.1789,
                'longitude': 27.6148,
                'fish_types': 'Crap, Caras, Roșioară',
                'facilities': 'parcare restaurant toalete',
                'rules': 'Pescuit doar cu permis. Interzis pescuitul noaptea.',
                'price_per_day': 40.00,
                'is_active': True
            },

            # Muntenia
            {
                'name': 'Balta Comana',
                'county_slug': 'giurgiu',
                'description': 'Complex de lacuri în Parcul Natural Comana.',
                'address': 'Comuna Comana, Județul Giurgiu',
                'latitude': 44.1742,
                'longitude': 26.1503,
                'fish_types': 'Crap, Caras, Știucă',
                'facilities': 'parcare restaurant toalete',
                'rules': 'Pescuit catch & release recomandat.',
                'price_per_day': 45.00,
                'is_active': True
            },

            # Transilvania
            {
                'name': 'Tarnița',
                'county_slug': 'cluj',
                'description': 'Lac de acumulare pe râul Someșul Cald.',
                'address': 'Comuna Gilău, Județul Cluj',
                'latitude': 46.7483,
                'longitude': 23.2727,
                'fish_types': 'Crap, Șalău, Clean, Păstrăv',
                'facilities': 'parcare cazare toalete',
                'rules': 'Permis necesar. Se permite pescuitul din barcă.',
                'price_per_day': 55.00,
                'is_active': True
            },

            # Dobrogea
            {
                'name': 'Lacul Siutghiol',
                'county_slug': 'constanta',
                'description': 'Lac natural lângă Mamaia, bogat în pește.',
                'address': 'Mamaia, Județul Constanța',
                'latitude': 44.2721,
                'longitude': 28.6198,
                'fish_types': 'Crap, Șalău, Biban, Plătică',
                'facilities': 'parcare cazare restaurant toalete',
                'rules': 'Necesită permis de pescuit. Zone speciale pentru pescuit sportiv.',
                'price_per_day': 60.00,
                'is_active': True
            },

            # Muntenia
            {
                'name': 'Lacul Budeasa',
                'county_slug': 'arges',
                'description': 'Lac de acumulare pe râul Argeș, cunoscut pentru pescuitul la crap și șalău.',
                'address': 'Comuna Budeasa, Județul Argeș',
                'latitude': 44.8584,
                'longitude': 24.8721,
                'fish_types': 'Crap, Șalău, Știucă',
                'facilities': 'parcare cazare toalete',
                'rules': 'Se permite pescuitul din barcă. Este necesară rezervare în avans.',
                'price_per_day': 60.00,
                'is_active': True
            },

            # Oltenia
            {
                'name': 'Lacul Zăton',
                'county_slug': 'mehedinti',
                'description': 'Complex piscicol format din mai multe lacuri.',
                'address': 'Comuna Bălăcița, Județul Mehedinți',
                'latitude': 44.4183,
                'longitude': 23.1189,
                'fish_types': 'Crap, Caras, Șalău, Amur',
                'facilities': 'parcare cazare toalete',
                'rules': 'Pescuit zi/noapte cu rezervare.',
                'price_per_day': 50.00,
                'is_active': True
            }
        ]

        # Create lakes
        for lake_data in lakes:
            county = County.objects.get(slug=lake_data.pop('county_slug'))
            lake, created = Lake.objects.get_or_create(
                name=lake_data['name'],
                county=county,
                defaults=lake_data
            )
            if created:
                self.stdout.write(f'Created lake: {lake.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created counties and lakes'))
