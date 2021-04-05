from django.shortcuts import render
from django.views.generic import (
    ListView,
)

from recipes.models import Recipe


class IndexView(ListView):
    model = Recipe
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
