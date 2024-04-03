from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"autofocus": True, "class": "form-control"}
    ))
    email = forms.EmailField(attrs={"class": "form-control"})
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
        attrs={"class": "form-control"}
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password",
        attrs={"class": "form-control"}
    )
