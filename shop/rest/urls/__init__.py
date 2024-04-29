from django.urls import path, include

urlpatterns = [
    path("", include("shop.rest.urls.shop")),
    path("", include("shop.rest.urls.member")),
]
