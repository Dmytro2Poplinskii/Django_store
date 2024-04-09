from django.contrib.auth.models import User
from django.db import models

CATEGORY_CHOICES = (
    ("CR", "Curd"),
    ("ML", "Milk"),
    ("LS", "Lassi"),
    ("MS", "Milkshake"),
    ("PN", "Panner"),
    ("GH", "Ghee"),
    ("CZ", "Cheese"),
    ("IC", "Ice-Greans"),
)

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
)


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    zip_code = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=3)

    def __str__(self) -> str:
        return f"{self.name}"
