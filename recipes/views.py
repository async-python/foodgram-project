from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from recipes.forms import RecipeForm
from recipes.models import Recipe, User, SubscriptionUser
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.http import HttpResponse
from api.views import get_session_key
from .services import get_list

paginate_count = 3


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'recipe_list'
    paginate_by = paginate_count

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.is_authenticated:
            context['favorites'] = Recipe.objects.select_related(
                'author').prefetch_related('tag').filter(
                favorite_recipe__user=self.request.user)
            context['shopping_list'] = Recipe.objects.filter(
                shopping_list__user=self.request.user)
        else:
            context['shopping_list'] = Recipe.objects.filter(
                shopping_list_session__session_id=
                get_session_key(self.request))
        return context

    def get_queryset(self):
        tags_values = self.request.GET.getlist('filters')
        if tags_values:
            return Recipe.objects.select_related(
                'author').prefetch_related('tag').filter(
                tag__name__in=tags_values).distinct()
        return Recipe.objects.select_related(
            'author').prefetch_related('tag').all()


class RecipeView(DetailView):
    model = Recipe
    template_name = 'single_page.html'
    pk_url_kwarg = 'recipe_id'
    query_pk_and_slug = ('recipe_id', 'username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.recipe_ingredients.all()
        if self.request.user.is_authenticated:
            context['is_favorite'] = self.object in Recipe.objects.filter(
                favorite_recipe__user=self.request.user)
            context['is_subscribe'] = SubscriptionUser.objects.filter(
                user=self.request.user, author=self.object.author).exists()
            context['shopping_list'] = Recipe.objects.filter(
                shopping_list__user=self.request.user)
        else:
            context['shopping_list'] = Recipe.objects.filter(
                shopping_list_session__session_id=
                get_session_key(self.request))
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'form_recipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form_recipe.html'
    form_class = RecipeForm
    pk_url_kwarg = 'recipe_id'
    query_pk_and_slug = ('recipe_id', 'username')

    def get_queryset(self):
        return Recipe.objects.select_related(
            'author').prefetch_related('tag').filter(author=self.request.user)

    def get_success_url(self):
        return reverse(
            'recipe',
            kwargs={'recipe_id': self.kwargs['recipe_id'],
                    'username': self.kwargs['username']}
        )


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'recipe_confirm_delete.html'
    model = Recipe
    pk_url_kwarg = 'recipe_id'
    query_pk_and_slug = ('recipe_id', 'username')
    success_url = reverse_lazy('index')


class UserRecipeList(LoginRequiredMixin, ListView):
    template_name = 'author_recipe.html'
    context_object_name = 'recipe_list'
    paginate_by = paginate_count

    def get_queryset(self):
        self.recipe_author = get_object_or_404(
            User, username=self.kwargs.get('username'))
        tags_values = self.request.GET.getlist('filters')
        if tags_values:
            return Recipe.objects.filter(
                author=self.recipe_author,
                tag__name__in=tags_values).distinct()
        return Recipe.objects.filter(author=self.recipe_author)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['recipe_author'] = self.recipe_author
        return context


class UserFollowList(LoginRequiredMixin, ListView):
    template_name = 'user_subscribe.html'
    context_object_name = 'subscriptions'
    paginate_by = paginate_count

    def get_queryset(self):
        return User.objects.prefetch_related('recipes').filter(
            following__user=self.request.user).annotate(
            count=Count('recipes')).order_by('-count')


class UserFavoritesList(LoginRequiredMixin, ListView):
    template_name = 'favorite.html'
    context_object_name = 'favorites'
    paginate_by = paginate_count

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['shopping_list'] = Recipe.objects.filter(
            shopping_list__user=self.request.user)
        return context

    def get_queryset(self):
        tags_values = self.request.GET.getlist('filters')
        if tags_values:
            return Recipe.objects.select_related(
                'author').prefetch_related('tag').filter(
                tag__name__in=tags_values,
                favorite_recipe__user=self.request.user).distinct()
        return Recipe.objects.select_related(
            'author').prefetch_related('tag').filter(
            favorite_recipe__user=self.request.user)


class UserPurchasesList(ListView):
    template_name = 'purchases.html'
    context_object_name = 'purchases'
    paginate_by = paginate_count

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.filter(shopping_list__user=self.request.user)
        return Recipe.objects.filter(
            shopping_list_session__session_id=get_session_key(self.request))


def get_purchases(request):
    response = HttpResponse(get_list(request), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=purchases.txt'
    return response


def page_not_found(request, exception):
    return render(
        request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
