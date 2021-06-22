from django import template

from api.utils import get_session_key
from recipes.models import Recipe, Tag

register = template.Library()


@register.filter(name='get_filter_values')
def get_filter_values(request):
    request._mutable = True
    filters = request.getlist('filters')
    filters = list(set(filters))
    if not len(filters):
        tags = Tag.objects.all()
        for tag in tags:
            filters.append(tag.name)
    request.setlist('filters', filters)
    request._mutable = False
    return filters


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    filters = request.GET.getlist('filters')
    if tag.name in filters:
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


@register.filter(name='url_parse')
def url_parse(request):
    result = ''
    for item in request.GET.getlist('filters'):
        result += f'&filters={item}'
    return result
