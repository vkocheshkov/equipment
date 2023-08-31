from django.test import TestCase

from equipment.models import EquipmentType
from equipment.serializers import EquipmentTypeSerializer


class EquipmentTypeSerializerTestCase(TestCase):
    def test_EquipmentTypeSerializer(self):
        """
        Тестирует рендеринг 1 записи из таблицы equipment_type после применения сериализатора EquipmentTypeSerializer
        """
        EquipmentType.objects.create(type_title="TP-Link TL-WR74", sn_mask="XXAAAAAXAA")
        query_data = EquipmentType.objects.filter(type_title="TP-Link TL-WR74").first()
        expected_data = {
            "id": query_data.id,
            "type_title": "TP-Link TL-WR74",
            "sn_mask": "XXAAAAAXAA",
        }
        validated_data = EquipmentTypeSerializer(query_data).data
        self.assertEquals(expected_data, validated_data)

    def test_EquipmentTypeSerializer_many(self):
        """
        Тестирует рендеринг нескольких записи из таблицы equipment_type после применения сериализатора
        EquipmentTypeSerializer с параметром many=True
        """
        EquipmentType.objects.create(type_title="TP-Link TL-WR74", sn_mask="XXAAAAAXAA")
        EquipmentType.objects.create(type_title="D-Link DIR-300", sn_mask="NXXAAXZXaa")
        query_data_1 = EquipmentType.objects.filter(type_title="TP-Link TL-WR74").first()
        query_data_2 = EquipmentType.objects.filter(type_title="D-Link DIR-300").first()
        expected_data = [
            {
                "id": query_data_1.id,
                "type_title": "TP-Link TL-WR74",
                "sn_mask": "XXAAAAAXAA",
            },
            {
                "id": query_data_2.id,
                "type_title": "D-Link DIR-300",
                "sn_mask": "NXXAAXZXaa",
            },
        ]
        query_data = EquipmentType.objects.all()
        validated_data = EquipmentTypeSerializer(query_data, many=True).data
        self.assertEquals(expected_data, validated_data)


