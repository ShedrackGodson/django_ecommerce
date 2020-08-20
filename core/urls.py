from .views import checkout, HomeView, ItemDetailView
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="item_list"),
    path('checkout/', checkout, name="checkout"),
    path('product/<slug>/detail/', ItemDetailView.as_view(), name="product"),
]
