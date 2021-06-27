from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from api.utils import get_session_key
from foodgram.settings import PAGINATOR_ITEMS_DISPLAY
from recipes.forms import RecipeForm
from recipes.models import Recipe, SubscriptionUser, User

from .services import get_list


class BaseListView(ListView):
    paginate_by = PAGINATOR_ITEMS_DISPLAY

    def get_filter_list(self):
        return self.request.GET.getlist('filters')


class IndexView(BaseListView):
    template_name = 'recipes/index.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        tags_values = self.get_filter_list()
        if tags_values:
            return Recipe.objects.select_related(
                'author').prefetch_related('tags').filter(
                tags__name__in=tags_values).distinct()
        return Recipe.objects.select_related(
            'author').prefetch_related('tags').all()


class RecipeView(DetailView):
    model = Recipe
    template_name = 'recipes/single_page.html'
    pk_url_kwarg = 'recipe_id'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        return get_object_or_404(
            Recipe, author__username=self.kwargs.get('username'),
            id=self.kwargs.get('recipe_id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.recipe_ingredients.all()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'recipes/form_recipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'recipes/form_recipe.html'
    form_class = RecipeForm
    pk_url_kwarg = 'recipe_id'

    def get_queryset(self):
        return get_recipes_queryset(self)

    def get_success_url(self):
        return reverse(
            'recipe',
            kwargs={'recipe_id': self.kwargs['recipe_id'],
                    'username': self.kwargs['username']}
        )


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'recipes/recipe_confirm_delete.html'
    model = Recipe
    pk_url_kwarg = 'recipe_id'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return get_recipes_queryset(self)


class UserRecipeList(BaseListView):
    template_name = 'recipes/author_recipe.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        self.recipe_author = get_object_or_404(
            User, username=self.kwargs.get('username'))
        tags_values = self.get_filter_list()
        if tags_values:
            return Recipe.objects.select_related(
                'author').prefetch_related('tags').filter(
                author=self.recipe_author,
                tags__name__in=tags_values).distinct()
        return Recipe.objects.select_related('author').prefetch_related(
            'tags').filter(author=self.recipe_author)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['author'] = self.recipe_author
        return context


class UserFollowList(LoginRequiredMixin, BaseListView):
    template_name = 'recipes/user_subscribe.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return User.objects.prefetch_related('recipes').filter(
            following__user=self.request.user).annotate(
            count=Count('recipes')).order_by('-count')


class UserFollowDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'recipes/subscribe_confirm_delete.html'
    context_object_name = 'subscription'
    pk_url_kwarg = 'author_id'
    query_pk_and_slug = True
    success_url = reverse_lazy('follow')

    def get_object(self, queryset=None):
        return get_object_or_404(
            SubscriptionUser,
            user=self.request.user,
            author_id=self.kwargs.get('author_id'))


class UserFavoritesList(LoginRequiredMixin, BaseListView):
    template_name = 'recipes/favorite.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        tags_values = self.get_filter_list()
        if tags_values:
            return Recipe.objects.select_related(
                'author').prefetch_related('tags').filter(
                tags__name__in=tags_values,
                favorite_recipe__user=self.request.user).distinct()
        return Recipe.objects.select_related(
            'author').prefetch_related('tags').filter(
            favorite_recipe__user=self.request.user)


class UserPurchasesList(ListView):
    template_name = 'recipes/purchases.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.filter(shopping_list__user=self.request.user)
        return Recipe.objects.filter(
            shopping_list_session__session_id=get_session_key(self.request))


def get_purchases(request):
    response = HttpResponse(get_list(request), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=purchases.txt'
    return response


def get_recipes_queryset(obj):
    if obj.request.user.username != obj.kwargs.get('username'):
        raise Http404("The link seems to be broken")
    return Recipe.objects.select_related(
        'author').prefetch_related(
        'tags', 'recipe_ingredients__ingredient').filter(
        author=obj.request.user)
