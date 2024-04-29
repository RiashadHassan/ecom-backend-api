from django.urls import path
from cart.rest.views.cart import (
    CartDetailView,
    CartItemListCreateView,
    ManageCartItemView,
)
from cart.rest.views.checkout import CheckoutView

urlpatterns = [
    path("/", CartDetailView.as_view(), name="cart-detail"),
    path("/items", CartItemListCreateView.as_view(), name="list-create-cart-items"),
    path(
        "/items/<uuid:cart_item_uuid>",
        ManageCartItemView.as_view(),
        name="manage-cart-item",
    ),
    path("/checkout", CheckoutView.as_view(), name="checkout"),
]
