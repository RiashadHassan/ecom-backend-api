from django.urls import path, include

urlpatterns = [
    path("", include("core.rest.urls.user")),
    path("/token", include("core.rest.urls.auth")),
]
