from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "discount_price", "category", "product_image")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location", "city", "state", "zip_code")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "order_id", "payment_status", "payment_id", "paid")


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "customer", "quantity", "ordered_date", "status", "payment")
