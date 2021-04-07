from django.shortcuts import render
from django.views.generic import (
    ListView,
)

from recipes.models import Recipe, Tag


class IndexView(ListView):
    model = Recipe
    template_name = 'index.html'
    context_object_name = "recipe_list"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


def page_not_found(request, exception):
    return render(
        request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
