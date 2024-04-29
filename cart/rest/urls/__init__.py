from django.urls import path, include

urlpatterns = [
    path("/me/cart", include("cart.rest.urls.cart")),
    #
]
