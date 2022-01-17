from django.contrib import admin # noqa
from customer.models import Customer
# Register your models here.


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


admin.site.register(Customer, StateAdmin)
