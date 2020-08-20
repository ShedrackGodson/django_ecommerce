from django.shortcuts import render
from .models import Order, OrderItem, Item
from django.views.generic import ListView, DetailView
# from django.core.urlresolvers import resolve


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"



def checkout(request):
    
    return render(request, "checkout-page.html", {
        
    })