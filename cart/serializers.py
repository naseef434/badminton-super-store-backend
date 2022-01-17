from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from cart.models import Cart, CartItem


class CartSerializer(ModelSerializer):
    items = SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_items(self, obj):
        cart_items = obj.cartitem_set.all()
        return CartItemSerializer(cart_items, many=True).data


class CartItemSerializer(ModelSerializer):
    product = StringRelatedField()

    class Meta:
        model = CartItem
        fields = '__all__'
