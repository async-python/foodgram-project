import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load template ingredients to database model Ingredient'

    def handle(self, *args, **options):
        with open('./ingredients.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    title=row[0],
                    dimension=row[1],
                )
