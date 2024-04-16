from django.http import HttpRequest

from .models import Cart, Wishlist


def total_wishlist_items_util(request: HttpRequest) -> tuple:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    return total_item, wishlist_item
