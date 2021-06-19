from django.contrib import admin

from .models import (FavoriteRecipe, Recipe, RecipeIngredient, ShoppingList,
                     ShoppingListSession, SubscriptionUser, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author', 'description', 'cooking_time', 'created',
    )
    list_display_links = ('pk', 'name')
    search_fields = ('name', 'author')
    list_filter = ('created',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color',)
    list_display_links = ('pk', 'name')
    list_filter = ('name', 'slug', 'color',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount',)
    list_display_links = ('pk', 'recipe')
    list_filter = ('recipe', 'ingredient',)


class SubscriptionsUsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')


class ShoppingListSessionAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'session')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(SubscriptionUser, SubscriptionsUsersAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(ShoppingListSession, ShoppingListSessionAdmin)
