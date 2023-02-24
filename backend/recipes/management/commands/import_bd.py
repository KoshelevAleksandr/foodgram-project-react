import os
from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag

file_ingredient = os.path.join(
    os.path.dirname(settings.BASE_DIR),
    'app/backend_static/data/ingredients.csv')
file_tags = os.path.join(
    os.path.dirname(settings.BASE_DIR),
    'app/backend_static/data/tags.csv')


class Command(BaseCommand):
    help = 'Импорт из csv файлов'

    def handle(self, *args, **options):

        with open(file_ingredient, encoding="utf-8") as csv_file:
            for row in DictReader(csv_file, delimiter=','):
                Ingredient.objects.get_or_create(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
            print('load ingredients')

        with open(file_tags, encoding="utf-8") as csv_file:
            for row in DictReader(csv_file, delimiter=','):
                Tag.objects.get_or_create(
                    name=row['name'],
                    color=row['color'],
                    slug=row['slug'],
                )
            print('load tags')
