from recipes.models import ShoppingList, ShoppingListSession, Tag


def purchases_processor(request):
    if request.user.is_authenticated:
        return {'purchases_count': ShoppingList.objects.filter(
            user=request.user).count()}
    return {'purchases_count': ShoppingListSession.objects.filter(
        session_id=request.session.session_key).count()}


def url_parse(request):
    result = []
    for item in request.GET.getlist('filters'):
        result += f'&filters={item}'
    return {'filters': ''.join(result)}


def all_tags(request):
    return {'all_tags': Tag.objects.all()}
