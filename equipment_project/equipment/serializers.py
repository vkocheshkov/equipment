from rest_framework.serializers import ModelSerializer

from equipment.models import EquipmentType


class EquipmentTypeSerializer(ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ("id", "type_title", "sn_mask")
