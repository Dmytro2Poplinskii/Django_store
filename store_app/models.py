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


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    composition = models.TextField(default="")
    prod_app = models.TextField(default="")
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    product_image = models.ImageField(upload_to="product")

    def __str__(self) -> str:
        return f"{self.title}"
