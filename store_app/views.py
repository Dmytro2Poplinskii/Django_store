from django.db.models import Q
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .models import Product, Customer, Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "app/home.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "app/about.html")


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "app/contact.html")


class CategoryView(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        products = Product.objects.filter(category=name)
        titles = Product.objects.filter(category=name).values("title")

        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        products = Product.objects.filter(title=name)
        titles = Product.objects.filter(category=products[0].category).values("title")

        return render(request, "app/category.html", locals())


class ProductDetail(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = Product.objects.get(pk=pk)

        return render(request, "app/product_detail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CustomerRegistrationForm()

        return render(request, "app/customer_registration.html", locals())

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully!")
        else:
            messages.warning(request, "Invalid input data, please try again.")

        return render(request, "app/customer_registration.html", locals())


class CustomerProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            location = form.cleaned_data["location"]
            city = form.cleaned_data["city"]
            phone = form.cleaned_data["phone"]
            state = form.cleaned_data["state"]
            zip_code = form.cleaned_data["zip_code"]

            customer = Customer(
                user=user,
                name=name,
                location=location,
                city=city,
                phone=phone,
                state=state,
                zip_code=zip_code,
            )

            customer.save()

            messages.success(request, "Your profile has been saved successfully!")
        else:
            messages.warning(request, "Invalid input data, please try again.")

        return render(request, "app/profile.html", locals())


def address(request: HttpRequest) -> HttpResponse:
    addresses = Customer.objects.filter(user=request.user)

    return render(request, "app/address.html", locals())


class UpdateAddressView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        user_address = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=user_address)

        return render(request, "app/update_address.html", locals())

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            customer = Customer.objects.get(pk=pk)
            customer.name = form.cleaned_data["name"]
            customer.location = form.cleaned_data["location"]
            customer.city = form.cleaned_data["city"]
            customer.phone = form.cleaned_data["phone"]
            customer.state = form.cleaned_data["state"]
            customer.zip_code = form.cleaned_data["zip_code"]

            customer.save()

            messages.success(request, "Your profile has been updated successfully!")
        else:
            messages.warning(request, "Invalid input data, please try again.")

        return redirect("store_app:address")


class CheckoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        addresses = Customer.objects.filter(user=user)
        carts = Cart.objects.filter(user=user)

        amount = 0

        for cart in carts:
            value = cart.quantity * cart.product.price_with_discount
            amount += value

        total_amount = amount + 4

        return render(request, "app/checkout.html", locals())


def add_to_cart(request: HttpRequest) -> HttpResponse:
    user = request.user
    product_id = request.GET.get("product_id", None)
    product = Product.objects.get(pk=product_id)

    Cart(user=user, product=product).save()

    return redirect("store_app:show-cart")


def show_cart(request: HttpRequest) -> HttpResponse:
    user = request.user
    carts = Cart.objects.filter(user=user)

    amount = 0

    for cart in carts:
        value = cart.product.price_with_discount * cart.quantity
        amount += value

    total_amount = amount + 4

    return render(request, "app/add_to_cart.html", locals())


def plus_cart(request: HttpRequest) -> JsonResponse:
    product_id = request.GET.get("product_id", None)
    cart = Cart.objects.get(Q(user=request.user) & Q(product=product_id))
    cart.quantity += 1
    cart.save()

    user = request.user
    carts = Cart.objects.filter(user=user)

    amount = 0

    for cart_item in carts:
        value = cart_item.product.price_with_discount * cart_item.quantity
        amount += value

    total_amount = amount + 4

    data = {
        "quantity": cart.quantity,
        "total_amount": total_amount,
        "amount": amount,
    }

    return JsonResponse(data)


def minus_cart(request: HttpRequest) -> JsonResponse:
    product_id = request.GET.get("product_id", None)
    cart = Cart.objects.get(Q(user=request.user) & Q(product=product_id))
    cart.quantity -= 1
    cart.save()

    user = request.user
    carts = Cart.objects.filter(user=user)

    amount = 0

    for cart_item in carts:
        value = cart_item.product.price_with_discount * cart_item.quantity
        amount += value

    total_amount = amount + 4

    data = {
        "quantity": cart.quantity,
        "total_amount": total_amount,
        "amount": amount,
    }

    return JsonResponse(data)


def remove_cart(request: HttpRequest) -> JsonResponse:
    product_id = request.GET.get("product_id", None)
    cart = Cart.objects.get(Q(user=request.user) & Q(product=product_id))
    cart.delete()

    user = request.user
    carts = Cart.objects.filter(user=user)

    amount = 0

    for cart_item in carts:
        value = cart_item.product.price_with_discount * cart_item.quantity
        amount += value

    total_amount = amount + 4

    data = {
        "quantity": cart.quantity,
        "total_amount": total_amount,
        "amount": amount,
    }

    return JsonResponse(data)
