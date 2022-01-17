from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import CartSerializer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @action(methods=['get'], detail=False)
    def get_cart(self, request):
        customer = request.user.customer
        cart, status = Cart.objects.get_or_create(owner=customer)
        return Response(data=self.serializer_class(cart).data)

    @action(methods=['post'], detail=False)
    def add_to_cart(self, request):
        customer = request.user.customer
        cart, status = Cart.objects.get_or_create(owner=customer)
        cart.add_product(**request.data)
        return Response(data=self.serializer_class(cart).data)

    @action(methods=['post'], detail=False)
    def delete_cart_item(self, request):
        customer = request.user.customer
        item = request.data.get('item')
        if not item:
            raise ValidationError(detail={'message': 'item required'})
        cart = Cart.objects.get(owner=customer)
        try:
            cart.delete_product(item)
        except ValueError:
            raise ValidationError(detail={'message': 'Mentioned item not found in customer cart'})
        return Response(data=self.serializer_class(cart).data)
