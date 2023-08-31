from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from accounts.admin import CustomUser
from equipment.models import EquipmentType


class EquipmentTypeViewSetTestCase(APITestCase):
    def setUp(self):
        username = "custom_user"
        password = "Qwerty!234"
        self.user = CustomUser.objects.create_user(username=username, password=password)

        jwt_fetch_data = {
            'username': username,
            'password': password,
        }

        url = reverse('login')
        response = self.client.post(url, jwt_fetch_data, format='json')
        token = response.data['tokens']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.get("access")}')

    def test_get_equipment_type_many(self):
        """
        Проверяет запрос на GET:/api/equipment-type, когда в базе много данных
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

        url = reverse("equipment-type-list")
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_data, response.data.get("results"))

    def test_get_equipment_type_one(self):
        """
        Проверяет запрос на GET:/api/equipment-type/1/ на выборку одной записи
        """
        EquipmentType.objects.create(type_title="TP-Link TL-WR74", sn_mask="XXAAAAAXAA")
        query_data = EquipmentType.objects.filter(type_title="TP-Link TL-WR74").first()
        expected_data = {
            "id": query_data.id,
            "type_title": "TP-Link TL-WR74",
            "sn_mask": "XXAAAAAXAA",
        }

        url = reverse("equipment-type-detail", args=(query_data.id,))
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_data, response.data)

    def test_get_equipment_type_filter(self):
        """
        Проверяет фильтрацию по ключам ответа позитивный и негативный случай
        """
        EquipmentType.objects.create(type_title="TP-Link TL-WR74", sn_mask="XXAAAAAXAA")
        query_data = EquipmentType.objects.filter(type_title="TP-Link TL-WR74").first()
        expected_data = [{
            "id": query_data.id,
            "type_title": "TP-Link TL-WR74",
            "sn_mask": "XXAAAAAXAA",
        }]

        url = reverse("equipment-type-list")
        url += f"?id={query_data.id}&type_title={expected_data[0]['type_title']}&sn_mask={expected_data[0]['sn_mask']}"
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_data, response.data.get("results"))

        url = reverse("equipment-type-list")
        url += f"?id={query_data.id}&type_title={expected_data[0]['type_title']}&sn_mask=XXX"
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        expected_data = []
        self.assertNotEquals(expected_data, response.data.get("results"))

    def test_unauthorized_access(self):
        """
        Проверяет, что неавторизированный доступ запрещен
        """
        client = APIClient()

        url = reverse("equipment-type-list")
        response = client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

        EquipmentType.objects.create(type_title="TP-Link TL-WR74", sn_mask="XXAAAAAXAA")
        query_data = EquipmentType.objects.filter(type_title="TP-Link TL-WR74").first()

        url = reverse("equipment-type-detail", args=(query_data.id,))
        response = client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

