from .views import checkout, HomeView, ItemDetailView, add_to_cart,remove_from_cart, \
    OrderSummaryView
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="item_list"),
    path('checkout/', checkout, name="checkout"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('product/<slug>/detail/', ItemDetailView.as_view(), name="product"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
]
