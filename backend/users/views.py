from api.serializers import CustomUserSerializer, CustomSreateUserSerializer
from api.serializers import SubscribeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from api.pagination import CustomPagination
from .models import Subscribe
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(author,
                                             data=request.data,
                                             context={"request": request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(Subscribe,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        # page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(queryset, many=True,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return self.get_paginated_response(serializer.data)
        # user_username = self.request.user
        # user = get_object_or_404(User, user=user_username)
        # subscribtions = user.subscribing.all()
        # return Response(request)
