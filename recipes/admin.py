from django.contrib import admin
from .models import Recipe, Tag, RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author', 'description', 'cooking_time', 'created',
    )
    list_display_links = ('pk', 'name')
    search_fields = ('name', 'author')
    list_filter = ('created',)
    empty_value_display = '-пусто-'

    # def show_ingredients(self, obj):
    #     return '\n'.join([a.ingredient for a in obj.recipe_ingredients.all()])


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color',)
    list_display_links = ('pk', 'name')
    list_filter = ('name', 'slug', 'color',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount',)
    list_display_links = ('pk', 'recipe')
    list_filter = ('recipe', 'ingredient',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
