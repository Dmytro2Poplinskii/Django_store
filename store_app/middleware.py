from django.http import HttpResponseRedirect
from django.urls import reverse


class RedirectNotLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != reverse("login"):
            return HttpResponseRedirect(reverse("login"))
        response = self.get_response(request)
        return response


class RedirectLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path != reverse("store_app:profile"):
            return HttpResponseRedirect(reverse("store_app:profile"))
        response = self.get_response(request)
        return response
