from django.contrib import admin
from payment.models import Item


@admin.register(Item)
class ShopAdmin(admin.ModelAdmin):
    pass
