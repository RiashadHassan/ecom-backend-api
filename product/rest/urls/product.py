from django.urls import path
from product.rest.views.product import *

urlpatterns = [
    # Private URLs
    path(
        "/we/shops/<uuid:shop_uuid>/products",
        ListCreateProductView.as_view(),
        name="list-create-products",
    ),
    # path(
    #     "/we/shop/products",
    #     DefaultShopProducts.as_view(),
    #     name="defualt-shop-products",
    # ),
    path(
        "/we/shops/<uuid:shop_uuid>/products/<uuid:product_uuid>",
        ManageProductView.as_view(),
        name="manage-products",
    ),
    # Public URLs
    path(
        "/me/shops/<slug:shop_slug>/products",
        ListProductView.as_view(),
        name="list-products",
    ),
    path(
        "/me/shops/<slug:shop_slug>/products/<slug:product_slug>",
        RetrieveProductView.as_view(),
        name="list-create-products",
    ),
]
