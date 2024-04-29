from django.urls import path, include

urlpatterns = [
    path("/me/orders", include("order.rest.urls.order")),
]
