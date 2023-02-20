from django.contrib import admin

from .models import Ingredient, IngredientsRecipes, Recipe, Tag


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('pub_date',)
    list_filter = ('author', 'name', 'tags',)


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(IngredientsRecipes)
class IngredientsRecipesAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    list_filter = ('recipe',)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
