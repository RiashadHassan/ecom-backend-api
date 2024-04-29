from django.urls import reverse


def product_create_url(shop_uuid: str):
    return reverse("list-create-products", args=[shop_uuid])


def product_update_url(shop_uuid: str, product_uuid: str):
    return reverse("manage-products", args=[shop_uuid, product_uuid])
