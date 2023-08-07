from django.core.management.base import BaseCommand
from relations.models import Product


class Command(BaseCommand):
    help = 'Create default product objects in the database.'

    def handle(self, *args, **options):
        # Create your default objects here
        Product.objects.bulk_create([
            Product(name="TR-1071-600A"),
            Product(name="TR-1071-1000A"),
            Product(name="TR-1071-1600A"),
            Product(name="TR 10071-1200A"),
            Product(name="TR 10071-1600A"),
            Product(name="TR 10071-2400A"),
            Product(name="TR 10071-3200A"),
            Product(name="TR 10071-4000A"),
            Product(name="TR 20023-1600A"),
            Product(name="TR 20023-2400A"),
            Product(name="TR 20023-3200A"),
            Product(name="TR 20023-4800A"),
            Product(name="TR 20023-6400A"),
            Product(name="TR 20023-8000A"),
            Product(name="TR 41915-9600A"),
            Product(name="TR 41915-12800A"),
            Product(name="TR 41915-16000A"),
            Product(name="TR 1453 Series"),
            Product(name="V7050"),
            Product(name="V7100"),
            Product(name="V7300"),
            Product(name="V7600"),
            Product(name="V7800"),
            Product(name="V7000S"),
        ])
