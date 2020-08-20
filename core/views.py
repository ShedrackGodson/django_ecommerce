from django.shortcuts import render
from .models import Order, OrderItem, Item
# from django.core.urlresolvers import resolve


def item_list(request):
    context = dict()
    context["items"] = Item.objects.all()
    return render(request, "home-page.html", context)


def products(request):

    return render(request, "product-page.html", {

    })


def checkout(request):
    
    return render(request, "checkout-page.html", {
        
    })