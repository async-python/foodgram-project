from rest_framework import serializers

from recipes.models import (FavoriteRecipe, Ingredient, ShoppingList,
                            ShoppingListSession, SubscriptionUser)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('title', 'dimension',)


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionUser
        fields = ('user', 'author')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('recipe', 'user')


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('recipe', 'user')


class PurchaseSerializerSession(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListSession
        fields = ('recipe', 'session')
