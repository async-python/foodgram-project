from abc import ABC

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from recipes.models import (
    Ingredient, SubscriptionUser, FavoriteRecipe, ShoppingList)
from rest_framework.validators import UniqueTogetherValidator


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
