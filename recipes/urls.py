from django.urls import path
from .views import IndexView, RecipeView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # path("feed/", views.feed, name="feed"),
    # path("new/", views.new_recipe, name="new"),
    # path("favorites/", views.favorites, name="favorites"),
    # path("wishlist/", views.wishlist, name="wishlist"),
    # path("<username>/", views.user_page, name="user"),
    path("<username>/<int:recipe_id>/", RecipeView.as_view(), name="recipe"),
    # path("<username>/<recipe_id>/edit/", views.edit_recipe,
    #      name="edit_recipe")
]
