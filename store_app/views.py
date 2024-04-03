from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from .models import Product


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "app/home.html")


class CategoryView(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        products = Product.objects.filter(category=name)
        title = Product.objects.filter(category=name).values("title").annotate(total=Count("title"))

        return render(request, "app/category.html", locals())


class ProductDetail(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = Product.objects.get(pk=pk)

        return render(request, "app/product_detail.html", locals())
