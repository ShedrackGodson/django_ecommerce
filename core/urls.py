from .views import CheckoutView, HomeView, ItemDetailView, add_to_cart,remove_from_cart, \
    OrderSummaryView,remove_single_item_from_cart,PaymentView
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="item_list"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('payment/<str:payment_option>/', PaymentView.as_view(), name="payment"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('product/<slug>/detail/', ItemDetailView.as_view(), name="product"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name="remove-single-item-from-cart"),
]


# pk_test_51HItOtLilkzwV54uYa8PVeEO81eYUWZmlvaaTwMay7T0ixCLW3eAW9eGBcP5in1tWyg8z8516QYHq02s8v1TNpNN00dPGv0cx5