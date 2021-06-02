from rest_framework import status, viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.filters import SearchFilter
from api.serializers import IngredientSerializer, SubscribeSerializer
from recipes.models import Ingredient, SubscriptionsUsers, User
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, DestroyModelMixin)
from rest_framework.viewsets import GenericViewSet
from api.permissions import IsOwnerOrAdmin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework.response import Response


class IngredientsViewSet(ListModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^title',)
    lookup_field = 'title'


class SubscribeCreateDeleteView(CreateModelMixin,
                                DestroyModelMixin, GenericViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def perform_create(self, serializer):
        author_id = self.request.data['id']
        author = get_object_or_404(User, pk=author_id)
        serializer.save(user=self.request.user, author=author)

    def get_object(self):
        obj = get_object_or_404(
            SubscriptionsUsers,
            author_id=self.kwargs.get('pk'),
            user_id=self.request.user.id)
        return obj
