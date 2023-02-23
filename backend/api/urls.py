from django.urls import include, path
from recipes.views import IngredientViewSet, RecipesViewSet, TagViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipesViewSet)
router.register('tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
