import base64
from recipes.models import Ingredient, IngredientsRecipes, Recipe, Tag
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers import CustomUserSerializer
from django.core.files.base import ContentFile
from drf_extra_fields import fields


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngredientsRecipesWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientsRecipes
        fields = (
            'id',
            'amount',
            )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
            )





class RecipesReadSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True,)
    image = fields.Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            )


class RecipesWriteSerializer(serializers.ModelSerializer):
    ingredients = IngredientsRecipesWriteSerializer(many=True,)
    author = serializers.PrimaryKeyRelatedField(read_only=True,)
    image = fields.Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            )

    def create(self, validate_data):
        ingredients = validate_data.pop('ingredients')
        tags = validate_data.pop('tags')
        recipe = Recipe.objects.create(**validate_data)
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get_or_create(
                ingredient[0])
            IngredientsRecipes.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredients['amount'])
        recipe.tags.set(tags)
        return recipe
