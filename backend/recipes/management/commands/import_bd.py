import os
from django.conf import settings
from csv import DictReader
from django.core.management.base import BaseCommand

from users.models import User
from recipes.models import Ingredient


file_ingredient = os.path.join(
    os.path.dirname(settings.BASE_DIR), 'data/ingredients.csv')


class Command(BaseCommand):
    help = 'Импорт из csv файлов'

    def handle(self, *args, **options):

        with open(file_ingredient, encoding="utf-8") as csv_file:
            for row in DictReader(csv_file, delimiter=','):
                ingredient = Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
                ingredient.save()
            print('load ingredients')