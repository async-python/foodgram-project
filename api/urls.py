from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientsViewSet, SubscribeCreateDeleteView

router = DefaultRouter()
router.register(r'ingredients', IngredientsViewSet)
router.register(
    r'subscriptions', SubscribeCreateDeleteView, basename='unsubscribe', )
# router.register(
#     r'subscriptions/(?P<author_id>[0-9]+)',
#     UnSubscribeView, basename='unsubscribe')

urlpatterns = [
    # path('subscriptions/<int:author_id>',
    #      UnSubscribeView.as_view(),
    #      name='remove_subscription'),
    # path('subscriptions/<int:author_id>',
    #      UnSubscribeView.as_view({'delete': 'destroy'}),
    #      name='remove_subscription'),
    # path('subscriptions/<int:author_id>',
    #      unfollowing, name='remove_subscription'),
    path('', include(router.urls)),
]

# urlpatterns = [
    # path("add_favorite",
    #      views.add_favorite, name="add_favorite"),
    # path("remove_favorite/<int:recipe_id>",
    #      views.remove_favorite, name="remove_favorite"),
    # path("add_wishlist",
    #      views.add_wishlist, name="add_wishlist"),
    # path("remove_wishlist/<int:recipe_id>",
    #      views.remove_wishlist, name="remove_wishlist"),
    # path("add_subscription",
    #      views.add_subscription, name="add_subscription"),
    # path("remove_subscription/<int:following_id>",
    #      views.remove_subscription, name="remove_subscription"),
    # path("<username>/<recipe_id>/remove/",
    #      views.remove_recipe, name="remove_recipe"),
    # path("ingredients/",
    #      IngredientsViewSet.as_view({'get': 'list'}), name="get_ingredients"),
    # path("print_wishlist/",
    #      views.get_wishlist, name="get_wishlist"),
# ]
