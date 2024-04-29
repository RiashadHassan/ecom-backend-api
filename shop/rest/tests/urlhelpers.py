from django.urls import reverse

"""PUBLIC ME URLS"""


def me_shop_list_create_url():
    return reverse("shops")


def me_shop_details_url():
    return reverse("retrieve-shop")


"""PRIVATE SHOP WE URLS"""


def we_update_delete_shop_url(shop_uuid: str):
    return reverse("manage-shop", args=[shop_uuid])


def we_get_last_updated_shop_url():
    return reverse("last-visited-shop")


def we_get_shop_list_url():
    return reverse("own-shops")


"""PRIVATE MEMBER URLS"""


def member_list_create_url(shop_uuid: str):
    return reverse("member-list-create", args=[shop_uuid])


def member_update_url(shop_uuid: str, member_uuid: str):
    return reverse("manage-shop-members", args=[shop_uuid, member_uuid])
