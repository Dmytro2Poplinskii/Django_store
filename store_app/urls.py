from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import forms

urlpatterns = [
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("category/<slug:name>", views.CategoryView.as_view(), name="category"),
    path("category-title/<name>", views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    path("profile/", views.CustomerProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("update-address/<int:pk>", views.UpdateAddressView.as_view(), name="update-address"),

    # login
    path("register/", views.CustomerRegistrationView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(
        template_name="app/login.html",
        authentication_form=forms.CustomerLoginForm
        ),
        name="login"
    ),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="app/password-reset.html", form_class=forms.CustomerPasswordResetForm
    ), name="password-reset"),
]

app_name = "store_app"
