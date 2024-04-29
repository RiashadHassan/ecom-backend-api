from django.urls import path
from shop.rest.views.shop import *

urlpatterns = [
    path("/we", ShopView.as_view(), name="last-visited-shop"),
    path("/we/shops", ListShopView.as_view(), name="own-shops"),
    path("/we/shops/<uuid:shop_uuid>", ManageShopView.as_view(), name="manage-shop"),
    path("/me/shops", ShopListCreateView.as_view(), name="shops"),
    path(
        "/me/shops/<slug:shop_slug>", RetrieveShopView.as_view(), name="retrieve-shop"
    ),
]
