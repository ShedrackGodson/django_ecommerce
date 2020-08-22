from django.db import models
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField



CATEGORY = (
    ('S', 'Shirt'),
    ('SW', 'Sport Wear'),
    ('OW', 'Out Wear')
)

LABEL = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY)
    label = models.CharField(max_length=1, choices=LABEL)
    slug = models.SlugField()
    description = models.TextField()
    # picture = models.ImageField(upload_to="items/")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})
    
    def add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})
    
    def remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug": self.slug})
    
    class Meta:
        ordering = [
            "-id"
        ]


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    

    def total_item_price(self)->int:
        return self.quantity * self.item.price
    
    def total_item_discount_price(self)->int:
        return self.quantity * self.item.discount_price
    
    def saving_amount(self)->int:
        return self.total_item_price() - self.total_item_discount_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.total_item_discount_price()
        else:
            return self.total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL,null=True,blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
            return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_final_price()
        
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = [
            "-id"
        ]
    

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = [
            "-id"
        ]
