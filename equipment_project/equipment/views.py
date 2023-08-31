from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from equipment.models import EquipmentType
from equipment.pagination import CustomPagination
from equipment.serializers import EquipmentTypeSerializer


class EquipmentTypeViewSet(ModelViewSet):
    """
    Отвечает за предоставление информации о доступных типах оборудования. Доступна пагинация, а также возможность
    поиска путем указания query параметров советующим ключам ответа.
    """
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "type_title", "sn_mask"]
    http_method_names = ["get"]
