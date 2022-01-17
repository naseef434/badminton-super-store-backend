from django.urls import include, path
from rest_framework.routers import DefaultRouter
from product.views import BrandViewSet, CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('brand', BrandViewSet)
router.register('product', ProductViewSet)
urlpatterns = [
    path('', include(router.urls))
]
