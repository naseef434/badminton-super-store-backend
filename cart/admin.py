from django.contrib import admin
from cart.models import Cart, CartItem
# Register your models here.

admin.site.register([Cart, CartItem])
