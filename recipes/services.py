from api.views import get_session_key
from recipes.models import Recipe
from django.db.models import Sum, F


def get_list(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(shopping_list__user=request.user)
    else:
        recipes = Recipe.objects.filter(
            shopping_list_session__session_id=get_session_key(request))
    result = []
    ingredient_list = recipes.values(
        title=F('ingredients__title'), dimension=F('ingredients__dimension'),
    ).annotate(amount=Sum('recipe_ingredients__amount')).order_by()
    for i in ingredient_list:
        item = (i.get('title'), str(i.get('amount')), i.get('dimension'))
        result += (' '.join(item)) + '\n'
    return result
