from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IngredientsViewSet, SubscribeCreateDeleteView,
    FavoritesCreateDeleteView, PurchaseListCreateDeleteView)

router = DefaultRouter()
router.register(r'ingredients', IngredientsViewSet)
router.register(
    r'subscriptions', SubscribeCreateDeleteView, basename='subscriptions_api')
router.register(
    r'favorites', FavoritesCreateDeleteView, basename='favorites_api')
router.register(
    r'purchases', PurchaseListCreateDeleteView, basename='purchases_api')

urlpatterns = [
    path('', include(router.urls)),
]
