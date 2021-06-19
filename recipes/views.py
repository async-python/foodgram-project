from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
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
    template_name = 'index.html'
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
    template_name = 'single_page.html'
    pk_url_kwarg = 'recipe_id'
    query_pk_and_slug = ('recipe_id', 'username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.recipe_ingredients.all()
        if self.request.user.is_authenticated:
            context['is_subscribe'] = SubscriptionUser.objects.filter(
                user=self.request.user, author=self.object.author).exists()
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
            'author').prefetch_related('tags').filter(author=self.request.user)

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


class UserRecipeList(LoginRequiredMixin, BaseListView):
    template_name = 'author_recipe.html'
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


class UserFollowList(LoginRequiredMixin, BaseListView):
    template_name = 'user_subscribe.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return User.objects.prefetch_related('recipes').filter(
            following__user=self.request.user).annotate(
            count=Count('recipes')).order_by('-count')


class UserFavoritesList(LoginRequiredMixin, BaseListView):
    template_name = 'favorite.html'
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


class UserPurchasesList(BaseListView):
    template_name = 'purchases.html'
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
