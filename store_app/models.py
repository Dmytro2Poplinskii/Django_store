from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from .choices import CATEGORY_CHOICES, STATE_CHOICES, STATUS_CHOICES


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    composition = models.TextField(default="")
    prod_app = models.TextField(default="")
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    product_image = models.ImageField(upload_to="product")

    @property
    def price_with_discount(self) -> float:
        return float(self.selling_price - self.discount_price)

    def __str__(self) -> str:
        return f"{self.title}"


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    zip_code = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=3)

    def __str__(self) -> str:
        return f"{self.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self) -> Decimal:
        return self.quantity * self.product.discount_price


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self) -> float:
        return self.quantity * self.product.price_with_discount


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
