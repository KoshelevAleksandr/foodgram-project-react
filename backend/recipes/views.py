from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Ingredient, Recipe, Tag
from api.serializers import IngredientSerializer, RecipesReadSerializer, RecipesWriteSerializer, TagSerializer
from api.pagination import CustomPagination


User = get_user_model()



class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesWriteSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipesWriteSerializer
        return RecipesReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
