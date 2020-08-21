from .views import checkout, HomeView, ItemDetailView, add_to_cart
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="item_list"),
    path('checkout/', checkout, name="checkout"),
    path('product/<slug>/detail/', ItemDetailView.as_view(), name="product"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
]
