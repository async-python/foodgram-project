from rest_framework.generics import get_object_or_404
from rest_framework.filters import SearchFilter
from api.serializers import (
    IngredientSerializer, SubscribeSerializer, FavoriteSerializer,
    PurchaseSerializer)
from recipes.models import (Ingredient, SubscriptionUser, User,
                            FavoriteRecipe, Recipe, ShoppingList)
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, DestroyModelMixin)
from rest_framework.viewsets import GenericViewSet
from api.permissions import IsOwnerOrAdmin


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

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=request.data['id'])
        data = {
            'user': request.user.id,
            'author': author.id
        }
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(
            SubscriptionUser,
            author_id=self.kwargs.get('pk'),
            user_id=self.request.user.id)
        return obj


class FavoritesCreateDeleteView(CreateModelMixin,
                                DestroyModelMixin, GenericViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=request.data['id'])
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(
            FavoriteRecipe,
            recipe_id=self.kwargs.get('pk'),
            user_id=self.request.user.id)
        return obj


class PurchaseListCreateDeleteView(ListModelMixin, CreateModelMixin,
                                   DestroyModelMixin, GenericViewSet):
    queryset = ShoppingList
    serializer_class = PurchaseSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=request.data['id'])
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(
            ShoppingList,
            recipe_id=self.kwargs.get('pk'),
            user_id=self.request.user.id)
        return obj
