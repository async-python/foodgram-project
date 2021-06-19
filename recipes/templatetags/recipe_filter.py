from django import template

from api.utils import get_session_key
from recipes.models import Recipe

register = template.Library()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.name in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters = list(set(filters))
        filters.remove(tag.name)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.name)
    return new_request.urlencode()


@register.filter
def get_favorites(user):
    if user.is_authenticated:
        return Recipe.objects.select_related(
            'author').prefetch_related('tags').filter(
            favorite_recipe__user=user)
    return None


@register.filter
def get_shopping_list(request):
    if request.user.is_authenticated:
        return Recipe.objects.filter(shopping_list__user=request.user)
    return Recipe.objects.filter(
        shopping_list_session__session_id=get_session_key(request))


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
