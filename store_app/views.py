from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "app/home.html")


class CategoryView(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        return render(request, "app/category.html", locals())
