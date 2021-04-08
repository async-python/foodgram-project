from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView
)

from recipes.models import Recipe, Tag, User


class IndexView(ListView):
    model = Recipe
    template_name = 'index.html'
    context_object_name = "recipe_list"
    paginate_by = 3


class RecipeView(DetailView):
    template_name = 'singlePage.html'
    context_object_name = 'single_recipe'

    def get_object(self, queryset=None):
        author = get_object_or_404(User, username=self.kwargs['username'])
        return get_object_or_404(author.recipes, id=self.kwargs['recipe_id'])


def page_not_found(request, exception):
    return render(
        request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
