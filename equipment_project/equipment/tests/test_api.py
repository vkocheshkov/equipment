from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from accounts.admin import CustomUser
from equipment.misc import present_datetime
from equipment.models import EquipmentType, Equipment


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
        self.assertTrue("count" in response.data)
        self.assertTrue("next" in response.data)
        self.assertTrue("previous" in response.data)

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


class EquipmentViewSetTestCase(APITestCase):
    def setUp(self):
        username = "custom_user"
        password = "Qwerty!234"
        self.user = CustomUser.objects.create_user(username=username, password=password)
        
        jwt_fetch_data = {
            "username": username,
            "password": password,
        }
        
        url = reverse("login")
        response = self.client.post(url, jwt_fetch_data, format="json")
        token = response.data["tokens"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.get("access")}')

        EquipmentType.objects.create(type_title="TP-Link TL-WR74", sn_mask="XXAAAAAXAA")
        self.equip_type = EquipmentType.objects.get(pk=1)

    def test_get_equipment_one(self):
        """
        Проверяет запрос на GET:/api/equipment/1/ на выборку одной записи
        """
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial")
        query_data = Equipment.objects.filter(serial_number="99AAAAA9AA").first()
        expected_data = {
            "id": query_data.id,
            "equipment_type": query_data.equipment_type.id,
            "serial_number": "99AAAAA9AA",
            "note": "Test serial",
            "created_at": present_datetime(query_data.created_at),
            "updated_at": present_datetime(query_data.updated_at)
        }

        url = reverse("equipment-detail", args=(query_data.id,))
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_data, response.data)

    def test_get_equipment_many(self):
        """
        Проверяет запрос на GET:/api/equipment, когда в базе много данных
        """
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial 1")
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="88AAAAA8AA", note="Test serial 2")
        query_data_1 = Equipment.objects.filter(serial_number="99AAAAA9AA").first()
        query_data_2 = Equipment.objects.filter(serial_number="88AAAAA8AA").first()
        expected_data = [
            {
                "id": query_data_1.id,
                "equipment_type": query_data_1.equipment_type.id,
                "serial_number": "99AAAAA9AA",
                "note": "Test serial 1",
                "created_at": present_datetime(query_data_1.created_at),
                "updated_at": present_datetime(query_data_1.updated_at)
            },
            {
                "id": query_data_2.id,
                "equipment_type": query_data_1.equipment_type.id,
                "serial_number": "88AAAAA8AA",
                "note": "Test serial 2",
                "created_at": present_datetime(query_data_2.created_at),
                "updated_at": present_datetime(query_data_2.updated_at)
            },
        ]

        url = reverse("equipment-list")
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_data, response.data.get("results"))
        self.assertTrue("count" in response.data)
        self.assertTrue("next" in response.data)
        self.assertTrue("previous" in response.data)

    def test_get_equipment_filter(self):
        """
        Проверяет фильтрацию по ключам ответа позитивный и негативный случай
        """
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial")
        query_data = Equipment.objects.filter(serial_number="99AAAAA9AA").first()
        expected_data = [{
            "id": query_data.id,
            "equipment_type": query_data.equipment_type.id,
            "serial_number": "99AAAAA9AA",
            "note": "Test serial",
            "created_at": present_datetime(query_data.created_at),
            "updated_at": present_datetime(query_data.updated_at)
        }]

        url = reverse("equipment-list")
        url += (f"?id={query_data.id}&equipment_type={expected_data[0]['equipment_type']}"
                f"&serial_number={expected_data[0]['serial_number']}&note={expected_data[0]['note']}")
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        data = response.data.get("results")
        self.assertEquals(expected_data, data)

        url = reverse("equipment-list")
        url += (f"?id={query_data.id}&equipment_type={expected_data[0]['equipment_type']}"
                f"&serial_number={expected_data[0]['serial_number']}&note=some")
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        expected_data = []
        self.assertNotEquals(expected_data, response.data.get("results"))

    def test_get_equipment_search(self):
        """
        Проверяет поиск по полю serial_number и полю note - позитивный и негативный случай
        """
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial")
        query_data = Equipment.objects.filter(serial_number="99AAAAA9AA").first()
        expected_data = [{
            "id": query_data.id,
            "equipment_type": query_data.equipment_type.id,
            "serial_number": "99AAAAA9AA",
            "note": "Test serial",
            "created_at": present_datetime(query_data.created_at),
            "updated_at": present_datetime(query_data.updated_at)
        }]

        url = reverse("equipment-list")
        url += "?search=99AAAAA9AA"
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_data, response.data.get("results"))

        url = reverse("equipment-list")
        url += "?search=serial"
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(expected_data, response.data.get("results"))

        url = reverse("equipment-list")
        url += "?search=BBBBBBB"

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        expected_data = []
        self.assertNotEquals(expected_data, response.data.get("results"))

    def test_unauthorized_access(self):
        """
        Проверяет, что неавторизированный доступ запрещен
        """
        client = APIClient()

        url = reverse("equipment-list")
        response = client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial")
        query_data = Equipment.objects.filter(serial_number="99AAAAA9AA").first()

        url = reverse("equipment-detail", args=(query_data.id,))
        response = client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_put(self):
        """
        Проверяет, что информация об объекте успешно обновляется
        """
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial")
        query_data = Equipment.objects.filter(serial_number="99AAAAA9AA").first()

        url = reverse("equipment-detail", args=(query_data.id,))
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        expected_data = response.data
        expected_data["serial_number"] = "11AAAAA1AA"
        expected_data["note"] = "put note"

        url = reverse("equipment-detail", args=(query_data.id,))
        response = self.client.put(url, data=expected_data, format="json")
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        url = reverse("equipment-detail", args=(query_data.id,))
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        self.assertEquals(expected_data, response.data)

    def test_delete(self):
        """
        Проверяет, что объект удаляется
        """
        Equipment.objects.create(equipment_type=self.equip_type, serial_number="99AAAAA9AA", note="Test serial")
        query_data = Equipment.objects.filter(serial_number="99AAAAA9AA").first()

        url = reverse("equipment-detail", args=(query_data.id,))
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        url = reverse("equipment-detail", args=(query_data.id,))
        response = self.client.delete(url, data={"format": "json"})
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

        url = reverse("equipment-detail", args=(query_data.id,))
        response = self.client.get(url, data={"format": "json"})
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create(self):
        """
        Проверяет, что создается новый серийный номер в базе данных после метода post
        """
        loaded_data = {
            "equipment_type": self.equip_type.id,
            "serial_numbers": ["99AAAAAXAA", "88AAAAAXAA"],
            "note": "Test note"
        }

        url = reverse("equipment-list")
        response = self.client.post(url, data=loaded_data, format="json")
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)



