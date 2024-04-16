from decimal import Decimal
import uuid
import pprint

from django.db.models import Q
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings

from .models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .liqpay import LiqPay


def home(request: HttpRequest) -> HttpResponse:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    return render(request, "app/home.html", locals())


def about(request: HttpRequest) -> HttpResponse:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    return render(request, "app/about.html", locals())


def contact(request: HttpRequest) -> HttpResponse:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    return render(request, "app/contact.html", locals())


class CategoryView(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        total_item = 0
        wishlist_item = 0

        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            wishlist_item = len(Wishlist.objects.filter(user=request.user))

        products = Product.objects.filter(category=name)
        titles = Product.objects.filter(category=name).values("title")

        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        total_item = 0
        wishlist_item = 0

        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            wishlist_item = len(Wishlist.objects.filter(user=request.user))

        products = Product.objects.filter(title=name)
        titles = Product.objects.filter(category=products[0].category).values("title")

        return render(request, "app/category.html", locals())


class ProductDetail(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        total_item = 0
        wishlist_item = 0

        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            wishlist_item = len(Wishlist.objects.filter(user=request.user))

        product = Product.objects.get(pk=pk)

        wishlist = Wishlist.objects.filter(product=product, user=request.user)

        return render(request, "app/product_detail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        total_item = 0
        wishlist_item = 0

        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            wishlist_item = len(Wishlist.objects.filter(user=request.user))

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
        total_item = 0
        wishlist_item = 0

        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            wishlist_item = len(Wishlist.objects.filter(user=request.user))

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
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    addresses = Customer.objects.filter(user=request.user)

    return render(request, "app/address.html", locals())


class UpdateAddressView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        total_item = 0
        wishlist_item = 0

        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            wishlist_item = len(Wishlist.objects.filter(user=request.user))

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
        total_item = 0
        wishlist_item = 0

        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            wishlist_item = len(Wishlist.objects.filter(user=request.user))

        user = request.user
        addresses = Customer.objects.filter(user=user)
        carts = Cart.objects.filter(user=user)

        amount = 0

        for cart in carts:
            value = cart.quantity * cart.product.price_with_discount
            amount += value

        total_amount = amount + 4

        return render(request, "app/checkout.html", locals())

    def post(self, request: HttpRequest) -> HttpResponse:
        total_amount = str(Decimal(request.POST.get("total_amount", 0)))
        liqpay = LiqPay(public_key=settings.PUBLIC_LIQPAY_KEY, private_key=settings.PRIVATE_LIQPAY_KEY)
        user = request.user

        order_id = str(uuid.uuid4())

        params = {
            "version": 3,
            "public_key": settings.PUBLIC_LIQPAY_KEY,
            "amount": total_amount,
            "currency": "USD",
            "description": f"Payment for order {order_id}",
            "order_id": order_id,
            "language": "en",
            "action": "pay",
            "result_url": "http://127.0.0.1:8000/store/payment-done/",
            "server_url": "http://127.0.0.1:8000/store/payment-done/",
        }

        response = liqpay.api(url="api/3/checkout", params=params)

        if response.status_code == 200:
            customer_id = request.POST.get("customer_id", None)
            customer = None

            if customer_id:
                customer = Customer.objects.get(pk=customer_id)
            else:
                messages.warning(request, "Please enter a valid address")

            payment_id = str(uuid.uuid4())

            payment = Payment(
                user=user,
                amount=total_amount,
                order_id=order_id,
                payment_status="pending",
                payment_id=payment_id,
            )
            payment.save()

            carts = Cart.objects.filter(user=user)

            for cart in carts:
                order_placed = OrderPlaced(
                    user=user,
                    customer=customer,
                    product=cart.product,
                    quantity=cart.quantity,
                    status="Pending",
                    payment=payment
                )

                order_placed.save()

            messages.success(request, "Your order has been created successfully!")

        return redirect(response.url)


def add_to_cart(request: HttpRequest) -> HttpResponse:
    user = request.user
    product_id = request.GET.get("product_id", None)
    product = Product.objects.get(pk=product_id)

    Cart(user=user, product=product).save()

    return redirect("store_app:show-cart")


def show_cart(request: HttpRequest) -> HttpResponse:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

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


def payment_done(request: HttpRequest) -> HttpResponse:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    return render(request, "app/payment_done.html", locals())


def orders(request: HttpRequest) -> HttpResponse:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    order_placed = OrderPlaced.objects.filter(user=request.user)

    return render(request, "app/orders.html", locals())


def plus_wishlist(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        product_id = request.GET.get("product_id", None)
        product = Product.objects.get(pk=product_id)
        user = request.user
        Wishlist(user=user, product=product).save()

        data = {
            "message": "Added to Wishlist!",
        }

        return JsonResponse(data)


def minus_wishlist(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        product_id = request.GET.get("product_id", None)
        product = Product.objects.get(pk=product_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()

        data = {
            "message": "Remove from Wishlist!",
        }

        return JsonResponse(data)


def search(request: HttpRequest) -> HttpResponse:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    query = request.GET.get("search", None)
    products = Product.objects.filter(title__icontains=query)

    return render(request, "app/search.html", locals())
