from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, pais_info, precio_final

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "products/<int:pk>/precio-final/",
        precio_final,
        name="producto-precio-final",
    ),
    path("soap/pais/", pais_info, name="soap-pais-info"),
]
