from django.urls import path

from .views import (IndexView, RecipeCreateView, RecipeDeleteView,
                    RecipeUpdateView, RecipeView, UserFavoritesList,
                    UserFollowDeleteView, UserFollowList, UserPurchasesList,
                    UserRecipeList, get_purchases)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('follow/', UserFollowList.as_view(), name="follow"),
    path('new/', RecipeCreateView.as_view(), name='new'),
    path('favorites/', UserFavoritesList.as_view(), name='favorites'),
    path('purchases/', UserPurchasesList.as_view(), name='purchases'),
    path(
        'delete_subscribe/<int:author_id>/',
        UserFollowDeleteView.as_view(), name='delete_subscribe'),
    path('download_list/', get_purchases, name='download_list'),
    path('<str:username>/', UserRecipeList.as_view(), name='user'),
    path('<str:username>/<int:recipe_id>/', RecipeView.as_view(),
         name='recipe'),
    path('<str:username>/<int:recipe_id>/edit/', RecipeUpdateView.as_view(),
         name='edit_recipe'),
    path('<str:username>/<int:recipe_id>/delete/', RecipeDeleteView.as_view(),
         name='delete_recipe'),
]
