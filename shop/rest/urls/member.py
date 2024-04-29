from django.urls import path
from shop.rest.views.member import *

urlpatterns = [
    # private URLs
    path(
        "/we/shops/<uuid:shop_uuid>/members",
        ShopMemberListCreateView.as_view(),
        name="member-list-create",
    ),
    path(
        "/we/shops/<uuid:shop_uuid>/members/<uuid:member_uuid>",
        ManageShopMemberView.as_view(),
        name="manage-shop-members",
    ),
]
