from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoritesCreateDeleteView, IngredientsViewSet,
                    PurchaseListCreateDeleteView, SubscribeCreateDeleteView)

router = DefaultRouter()
router.register(r'ingredients', IngredientsViewSet)
router.register(
    r'subscriptions', SubscribeCreateDeleteView, basename='subscriptions_api')
router.register(
    r'favorites', FavoritesCreateDeleteView, basename='favorites_api')
router.register(
    r'purchases', PurchaseListCreateDeleteView, basename='purchases_api')

urlpatterns = [
    path('v1/', include(router.urls)),
]
