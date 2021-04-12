from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from api.serializers import IngredientSerializer
from recipes.models import Ingredient
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, DestroyModelMixin)
from rest_framework.viewsets import GenericViewSet


class IngredientsViewSet(ListModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('title',)
    lookup_field = 'title'
