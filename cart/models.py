from django.db import models
from product.models import Product, Variant
from customer.models import Customer
# Create your models here.


class Cart(models.Model):
    owner = models.OneToOneField(Customer, on_delete=models.CASCADE)
    item_count = models.IntegerField(default=0)
    total = models.FloatField(default=0)

    def add_product(self, product_id, variant_id=None, quantity=1):
        """
        if variant id is provides price & details populated from variant table.
        if product already present in cart update quantity & total.
        """
        product = Product.objects.get(id=product_id)
        is_variant = False
        if variant_id:
            variant = Variant.objects.get(id=variant_id)
            size = variant.size
            color = variant.color
            price = variant.price
            is_variant = True
        else:
            size = product.size
            color = product.color
            price = product.price
        total = price * quantity
        size = str(size) if size else None
        color = str(color) if color else None
        cart_item = CartItem.objects.filter(cart=self, product_id=product_id, size=size, color=color)
        if cart_item:
            # product already in cart update quanity and price
            cart_item[0].quantity += quantity
            cart_item[0].total += total
            cart_item[0].save()
        else:
            CartItem.objects.create(cart=self, product_id=product_id, price=price, total=total,
                                    quantity=quantity, size=size, color=color, is_variant=is_variant)
        self.item_count += 1
        self.total += total
        self.save()

    def delete_product(self, cart_item_id: int):
        try:
            item = CartItem.objects.get(id=cart_item_id)
        except Exception:
            raise ValueError('Item not found')
        self.total -= item.total
        self.item_count -= 1
        self.save()
        item.delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.TextField(max_length=60, null=True, blank=True)
    size = models.TextField(max_length=60, null=True, blank=True)
    is_variant = models.BooleanField(default=False)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
