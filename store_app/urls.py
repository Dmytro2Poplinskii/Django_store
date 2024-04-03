from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("category/<slug:name>", views.CategoryView.as_view(), name="category"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
]

app_name = "store_app"
