import base64
from recipes.models import Ingredient, IngredientsRecipes, Recipe, Tag
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from users.models import Subscribe
from users.serializers import CustomUserSerializer
from django.core.files.base import ContentFile
from drf_extra_fields import fields
from rest_framework.exceptions import ValidationError

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
    ingredients = IngredientSerializer
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


class RecipeShortSerializer(serializers.ModelSerializer):
    image = fields.Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(CustomUserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes_count', 'recipes'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortSerializer(recipes, many=True, read_only=True)
        return serializer.data
