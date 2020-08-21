from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem, Item
from django.views.generic import ListView, DetailView
from django.utils import timezone
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


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        
        else:
            order.item.add((order_item))

    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.item.add(order_item)
    
    return redirect("core:product", slug=slug)