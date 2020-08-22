from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem, Item, BillingAddress, Payment
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
# from django.core.urlresolvers import resolve


import stripe
stripe.api_key = "sk_test_51HItOtLilkzwV54uwf5LfpsQp6302tMZS2bOMjb9S9XaqOmuJNPQEmUseDupisP55UOV3knPneAVOaZXsqQlqKjR00CdeIMoqO"




class HomeView(ListView):
    model = Item
    paginate_by = 16
    template_name = "home-page.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(
                self.request, "You do not have an active order.",
                fail_silently=False
            )
            return redirect("/")


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "product-page.html"



class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
    
        return render(self.request, "checkout-page.html", {
            "form": CheckoutForm()
        })
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get("street_address")
                appartment_address = form.cleaned_data.get("appartment_address")
                country = form.cleaned_data.get("country")
                zip_code = form.cleaned_data.get("zip_code")
                # TODO : Adding the functionality for this fields 

                # save_info = form.cleaned_data.get("save_info")
                # same_shipping_address = form.cleaned_data.get("same_shipping_address")

                payment_option = form.cleaned_data.get("payment_option")

                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = appartment_address,
                    country = country,
                    zip_code = zip_code
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                
                if payment_option == 'S':
                    return redirect("core:payment", payment_option="stripe")
                elif payment_option == 'P':
                    return redirect("core:payment", payment_option="paypal")
                else:
                    messages.warning(self.request, "Invalid payment option.", fail_silently=False)
                    return redirect("core:checkout")

        except ObjectDoesNotExist:
            
            messages.warning(self.request, "You do not have an active order.", fail_silently=False)
            return redirect("core:order-summary")


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, "payment.html",{
            "order": Order.objects.get(user=self.request.user, ordered=False)
        })

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100 ) # Values are in Cents:

        try:
            charge = stripe.Charge.create(
                amount=amount, 
                currency="tzs",
                source=token
                # description="My First Test Charge (created for API docs)",
            )

            # Create The Payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = int(order.get_total())
            payment.save()

            # Assign Payment to the Order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order is successfully!", fail_silently=False)
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

            # print('Status is: %s' % e.http_status)
            # print('Type is: %s' % e.error.type)
            # print('Code is: %s' % e.error.code)
            # # param is '' in this case
            # print('Param is: %s' % e.error.param)
            # print('Message is: %s' % e.error.message)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error.")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.error(self.request, "Invalid Parameters.{}".format(e))
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Failed to authenticate with Stripe.")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Failed Stripe API connection. Check out network connection.")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong.")
            return redirect("/")
        except Exception as e:
            # Send an email to myself
            messages.error(self.request, "A serious error occured. We've emailed you instructions.")
            return redirect("/")


@login_required
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
            # messages.success(
            #     request, "This Item quantity is updated successfully.", fail_silently=False
            # )
            return redirect("core:order-summary")
        
        else:
            order.item.add((order_item))
            messages.success(request,
            "You have successfully added an item to the cart.", fail_silently=False
            )
            return redirect("core:order-summary")

    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.item.add(order_item)
    
    return redirect("core:order-summary")


@login_required
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
            return redirect("core:order-summary")
        
        else:
            # Adding a message saying that the order doesn't contain this OrderItem
            messages.info(request, "Your Order doesn't contains an Item.", fail_silently=False)
            return redirect("core:product")

    else:
        # Adding a message saying a user doesnt have an order
        messages.info(request, "You don't seems to have an Order yet!.", fail_silently=False)
        return redirect("core:product", slug=slug)

    return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.remove(order_item)
            # messages.success(
            #     request, "This item quantity was updated.", fail_silently=False
            #     )
            return redirect("core:order-summary")

        else:
            # Adding a message saying that the order doesn't contain this OrderItem
            messages.info(request, "Your Order doesn't contains an Item.", fail_silently=False)
            return redirect("core:order-summary", slug=slug)

    else:
        # Adding a message saying a user doesnt have an order
        messages.info(request, "You don't seems to have an Order yet!.", fail_silently=False)
        return redirect("core:product", slug=slug)

    return redirect("core:product", slug=slug)
