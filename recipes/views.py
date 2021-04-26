from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)

from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag, User
from django.urls import reverse


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
    form_class = RecipeForm
    success_url = 'index'

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        form_obj.author = self.request.user
        form_obj.save()
        form.save_m2m()
        return redirect(self.success_url)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'formRecipe.html'
    form_class = RecipeForm

    def get_object(self, queryset=None):
        author = get_object_or_404(User, username=self.kwargs['username'])
        return get_object_or_404(author.recipes, id=self.kwargs['recipe_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_recipe'] = True
        return context

    def get_success_url(self):
        return reverse(
            'recipe',
            kwargs={'recipe_id': self.kwargs['recipe_id'],
                    'username': self.kwargs['username']}
        )


def page_not_found(request, exception):
    return render(
        request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
