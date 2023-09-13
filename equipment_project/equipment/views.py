from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from equipment.models import Equipment, EquipmentType
from equipment.pagination import CustomPagination
from equipment.serializers import (
    EquipmentCreateSerializer,
    EquipmentSerializer,
    EquipmentTypeSerializer,
)
from equipment.service import check_serial_numbers_for_errors


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


class EquipmentViewSet(ModelViewSet):
    """
    Отвечает за предоставление информации о доступных серийных номерах оборудования. Доступна пагинация, а также
     возможность поиска путем указания query параметров советующим ключам ответа.
    """

    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "equipment_type", "serial_number", "note"]
    search_fields = ["serial_number", "note"]
    http_method_names = ["get", "post", "put", "delete"]

    def create(self, request, *args, **kwargs):
        serializer = EquipmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        data = {
            "equipment_type": request.data.get("equipment_type", None),
            "serial_number": request.data.get("serial_number", None),
            "note": request.data.get("note", None),
        }
        errors = check_serial_numbers_for_errors([data.get("serial_number")], data.get("equipment_type"))
        if errors:
            raise ValidationError({"serial_number": errors})
        serializer = self.serializer_class(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError(serializer.errors)
