from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from equipment.models import Equipment, EquipmentType
from equipment.service import check_serial_numbers_for_errors


class EquipmentTypeSerializer(ModelSerializer):
    """
    Отвечает за представление данных по таблице EquipmentType
    """

    class Meta:
        model = EquipmentType
        fields = ("id", "type_title", "sn_mask")


class EquipmentSerializer(ModelSerializer):
    """
    Отвечает за представление данных по таблице Equipment
    """

    class Meta:
        model = Equipment
        fields = ("id", "equipment_type", "serial_number", "note", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class EquipmentCreateSerializer(ModelSerializer):
    """
    Отвечает за десереализацию данных при сохранении объекта оборудования, с учетом того, что в полу serial_numbers
     может передаваться список серийных номеров
    """

    serial_numbers = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Equipment
        fields = ("equipment_type", "serial_numbers", "note")

    # Redefine is_valid and save methods

    def validate_serial_numbers(self, value):
        """
        Проверяет на соответствие серийного номера маске, а так же на уникальность данных в таблице Equipment учетом
        полей equipment_type и serial_number
        """
        equipment_type = self.initial_data.get("equipment_type")
        errors = check_serial_numbers_for_errors(value, equipment_type)

        if errors:
            raise ValidationError(errors)
        else:
            return value

    def create(self, validated_data):
        """
        Добавляет серийные номера в таблицу Equipment
        """
        Equipment.add_equipment(validated_data)
        return validated_data
