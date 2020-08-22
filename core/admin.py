from django.contrib import admin

from .models import Order, OrderItem, Item, BillingAddress, Payment


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user", "ordered"
    )

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(BillingAddress)
admin.site.register(Payment)
