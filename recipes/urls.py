from django.urls import path
from .views import IndexView, RecipeView, RecipeCreateView, RecipeUpdateView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # path("feed/", views.feed, name="feed"),
    path("new/", RecipeCreateView.as_view(), name="new"),
    # path("favorites/", views.favorites, name="favorites"),
    # path("wishlist/", views.wishlist, name="wishlist"),
    # path("<username>/", views.user_page, name="user"),
    path("<str:username>/<int:recipe_id>/", RecipeView.as_view(),
         name="recipe"),
    path("<str:username>/<int:recipe_id>/edit/", RecipeUpdateView.as_view(),
         name="edit_recipe")
]
