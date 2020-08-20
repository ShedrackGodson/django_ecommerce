from django.shortcuts import render
from .models import Order, OrderItem, Item


def item_list(request):
    context = dict()
    context["items"] = Item.objects.all()
    return render(request, "item_list.html", context)
