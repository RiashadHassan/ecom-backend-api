from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("rest_framework.urls")),
    # SWAGGER API
    path("api/schema", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("check-response/", include("silk.urls", namespace="silk")),
    # ProjectAPPs
    path("api/v1", include("core.rest.urls")),
    # path("api/v1/auth",include('core.rest.urls.auth')),
    path("api/v1", include("shop.rest.urls")),
    path("api/v1", include("product.rest.urls")),
    path("api/v1", include("cart.rest.urls")),
    path("api/v1", include("order.rest.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
