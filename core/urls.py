from .views import item_list, products, checkout
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', item_list, name="item_list"),
    path('checkout/', checkout, name="checkout"),
    path('product/', products, name="product"),
]
