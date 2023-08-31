from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from equipment import views

router = routers.DefaultRouter()
router.register(r"equipment-type", views.EquipmentTypeViewSet, basename="equipment-type")
# router.register(r"key", views.DLMSMeterKeysViewSet, basename="keys")

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

urlpatterns += router.urls
