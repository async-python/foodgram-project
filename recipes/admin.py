from django.contrib import admin
from .models import Recipe, Tag


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


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
