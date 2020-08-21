from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem, Item
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib import messages
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
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(
                request, "This Item quantity is updated successfully.", fail_silently=False
            )
        
        else:
            order.item.add((order_item))
            messages.success(request,
            "You have successfully added an item to the cart.", fail_silently=False
            )

    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.item.add(order_item)
    
    return redirect("core:product", slug=slug)



def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # print(item.slug)

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        # print(order.item.filter(item__slug=item.slug))
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # print("Exists.")

            order.item.remove(order_item)
            messages.success(
                request, "You have successfully removed an item from the cart.", fail_silently=False
                )
        
        else:
            # Adding a message saying that the order doesn't contain this OrderItem
            messages.info(request, "Your Order doesn't contains an Item.", fail_silently=False)
            return redirect("core:product", slug=slug)

    else:
        # Adding a message saying a user doesnt have an order
        messages.info(request, "You don't seems to have an Order yet!.", fail_silently=False)
        return redirect("core:product", slug=slug)

    return redirect("core:product", slug=slug)