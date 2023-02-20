from users.serializers import CustomSreateUserSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from api.pagination import CustomPagination


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomSreateUserSerializer
    pagination_class = CustomPagination
