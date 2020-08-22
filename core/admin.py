from django.contrib import admin

from .models import Order, OrderItem, Item, BillingAddress, Payment


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(BillingAddress)
admin.site.register(Payment)
