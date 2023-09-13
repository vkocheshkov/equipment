from django.test import TestCase

from equipment.misc import present_datetime
from equipment.models import EquipmentType, Equipment
from equipment.serializers import EquipmentTypeSerializer, EquipmentSerializer, EquipmentCreateSerializer


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


class EquipmentSerializerTestCase(TestCase):
    def setUp(self):
        EquipmentType.objects.create(type_title="TP-Link TL-WR74", sn_mask="XXAAAAAXAA")
        self.equip_type = EquipmentType.objects.get(pk=1)

    def test_get_one(self):
        """
        Тестирует рендеринг 1 записи из таблицы equipment после применения сериализатора EquipmentSerializer
        """
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial")
        query_data = Equipment.objects.all().first()
        expected_data = {
            "id": query_data.id,
            "equipment_type": self.equip_type.id,
            "serial_number": "99AAAAA9AA",
            "note": "Test serial",
            "created_at": present_datetime(query_data.created_at),
            "updated_at": present_datetime(query_data.updated_at)
        }

        validated_data = EquipmentSerializer(query_data).data
        self.assertEquals(expected_data, validated_data)

    def test_get_many(self):
        """
        Тестирует рендеринг нескольких записи из таблицы equipment после применения сериализатора
        EquipmentSerializer с параметром many=True
        """
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial 1")
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="88AAAAA8AA", note="Test serial 2")
        query_data_1 = Equipment.objects.filter(serial_number="99AAAAA9AA").first()
        query_data_2 = Equipment.objects.filter(serial_number="88AAAAA8AA").first()
        expected_data = [
            {
                "id": query_data_1.id,
                "equipment_type": self.equip_type.id,
                "serial_number": "99AAAAA9AA",
                "note": "Test serial 1",
                "created_at": present_datetime(query_data_1.created_at),
                "updated_at": present_datetime(query_data_1.updated_at)
            },
            {
                "id": query_data_2.id,
                "equipment_type": self.equip_type.id,
                "serial_number": "88AAAAA8AA",
                "note": "Test serial 2",
                "created_at": present_datetime(query_data_2.created_at),
                "updated_at": present_datetime(query_data_2.updated_at)
            },
        ]
        query_data = Equipment.objects.all()
        validated_data = EquipmentSerializer(query_data, many=True).data
        self.assertEquals(expected_data, validated_data)


class EquipmentCreateSerializerTestCase(TestCase):
    def setUp(self):
        EquipmentType.objects.create(type_title="TP-Link TL-WR74", sn_mask="XXAAAAAXAA")
        self.equip_type = EquipmentType.objects.get(pk=1)

    def test_deserialization(self):
        data = {
            "equipment_type": self.equip_type.id,
            "serial_numbers": ["XXAAAAAXAA", "XYAAAAAXAA"],
            "note": "Test note"
        }
        serializer = EquipmentCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        query_data = Equipment.objects.filter(serial_number="XXAAAAAXAA").first()
        data_repr = EquipmentSerializer(query_data).data
        expected_data = {
            "id": query_data.id,
            "equipment_type": self.equip_type.id,
            "serial_number": "XXAAAAAXAA",
            "note": "Test note",
            "created_at": present_datetime(query_data.created_at),
            "updated_at": present_datetime(query_data.updated_at)
        }
        self.assertEquals(expected_data, data_repr)



