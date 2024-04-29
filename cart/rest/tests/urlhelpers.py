from django.urls import reverse

"""CART APP URLS"""


def get_user_cart():
    return reverse("cart-detail")


def get_list_create_cart_items():
    return reverse("list-create-cart-items")


"""ORDER APP URLS"""


def order_list_url():
    return reverse("orders")


def order_create_url():
    return reverse("checkout")


def order_items_list_url():
    return reverse("order-items")


def order_items_detail_url(order_item_uuid: str):
    return reverse("order-items-detail", args=[order_item_uuid])


def order_item_review_url(order_item_uuid: str):
    return reverse("order-items-detail", args=[order_item_uuid])
