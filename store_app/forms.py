from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"autofocus": True, "class": "form-control"}
    ))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
