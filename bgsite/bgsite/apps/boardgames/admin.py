# pylint: skip-file

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import BoardGame, Customer, Cart, CartProduct


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = "Покупатели"


class UserAdmin(BaseUserAdmin):
    inlines = [
        CustomerInline,
    ]


admin.site.register(BoardGame)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct)
