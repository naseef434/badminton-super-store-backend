from django.db import models
from django.contrib.auth import get_user_model


class Customer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='phone')
    name = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address_line1 = models.CharField(max_length=50, null=True, blank=True)
    address_line2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
