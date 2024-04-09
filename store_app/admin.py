from django.contrib import admin
from .models import Product, Customer


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "discount_price", "category", "product_image")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location", "city", "state", "zip_code")
