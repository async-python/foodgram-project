from abc import ABC

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from recipes.models import Ingredient, SubscriptionsUsers, User
from rest_framework.validators import UniqueTogetherValidator


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('title', 'dimension',)


class SubscribeSerializer(serializers.Serializer):
    def create(self, validated_data):
        return SubscriptionsUsers.objects.create(**validated_data)

    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    # author = serializers.PrimaryKeyRelatedField(read_only=True)

    # class Meta:
        # model = SubscriptionsUsers
        # fields = ('user', 'author')
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=SubscriptionsUsers.objects.all(),
        #         fields=['user', 'author']
        #     )
        # ]
