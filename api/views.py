from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsOwnerOrAdmin
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             PurchaseSerializer, PurchaseSerializerSession,
                             SubscribeSerializer)
from api.utils import get_session_key
from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingList,
                            ShoppingListSession, SubscriptionUser, User)


class IngredientsViewSet(ListModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^title',)
    lookup_field = 'title'


class BaseCreateDeleteView(CreateModelMixin,
                           DestroyModelMixin, GenericViewSet):
    permission_classes = (IsOwnerOrAdmin,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        success = instance.delete()
        return Response({'success': bool(success)}, status=status.HTTP_200_OK)


class SubscribeCreateDeleteView(BaseCreateDeleteView):
    serializer_class = SubscribeSerializer

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=request.data.get('id'))
        data = {'user': request.user.id, 'author': author.id}
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(
            SubscriptionUser,
            author_id=self.kwargs.get('pk'),
            user_id=self.request.user.id)


class FavoritesCreateDeleteView(BaseCreateDeleteView):
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=request.data.get('id'))
        data = {'user': request.user.id, 'recipe': recipe.id}
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(
            FavoriteRecipe,
            recipe_id=self.kwargs.get('pk'),
            user_id=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        success = instance.delete()
        return Response({'success': bool(success)}, status=status.HTTP_200_OK)


class PurchaseListCreateDeleteView(ListModelMixin, CreateModelMixin,
                                   DestroyModelMixin, GenericViewSet):

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return PurchaseSerializer
        return PurchaseSerializerSession

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ShoppingList
        return ShoppingListSession

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=request.data.get('id'))
        if self.request.user.is_authenticated:
            data = {'user': self.request.user.id, 'recipe': recipe.id}
        else:
            data = {'session': get_session_key(request), 'recipe': recipe.id}
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def get_object(self):
        if self.request.user.is_authenticated:
            return get_object_or_404(
                ShoppingList,
                recipe_id=self.kwargs.get('pk'),
                user_id=self.request.user.id)
        return get_object_or_404(
            ShoppingListSession,
            recipe_id=self.kwargs.get('pk'),
            session_id=get_session_key(self.request))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        success = instance.delete()
        return Response({'success': bool(success)}, status=status.HTTP_200_OK)
