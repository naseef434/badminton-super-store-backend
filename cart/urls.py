from django.urls import include, path
from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet

router = DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
urlpatterns = [
    path('', include(router.urls))
]
