from django.contrib import admin

from .models import Customer

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)