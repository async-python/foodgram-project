from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView
)

from recipes.forms import RecipeForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.recipe_ingredients.all()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'formRecipe.html'
    # context_object_name = 'recipe_create'
    form_class = RecipeForm
    success_url = 'index'

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        form_obj['author'] = self.request.user
        form_obj.save()
        return redirect('index')

    def form_invalid(self, form):
        return render(self.request, 'formRecipe.html',
                      {'form': form, })


def page_not_found(request, exception):
    return render(
        request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
