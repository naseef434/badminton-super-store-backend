from rest_framework import viewsets
from rest_framework.decorators import action
from product.serializers import CategorySerializer, BrandSerializer, ProductSerializer
from product.models import Category, Brand, Product


class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = None
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BrandViewSet(viewsets.ModelViewSet):
    pagination_class = None
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(quantity__gt=0)
    filterset_fields = ['category', 'brand']

    @action(methods=["GET"], detail=False)
    def sale(self, request):
        queryset = self.queryset.filter(sale_price__isnull=False)
        page = self.paginate_queryset(queryset)
        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )
        response = self.get_paginated_response(serializer.data)
        return response
