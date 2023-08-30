from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from accounts.admin import CustomUser


class AuthViewsTests(APITestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(username="custom_user", password="Qwerty!234")

    def test_login_negative_password(self):
        """
        Проверяет, что с неверным паролем залогиниться нельзя
        Returns: None
        """
        credentials_data = {"username": "custom_user", "password": "11111111111"}
        url = reverse("login")
        response = self.client.post(url, data=credentials_data, format="json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_negative_username(self):
        """
        Проверяет, что с неверным паролем залогиниться нельзя
        Returns: None
        """
        credentials_data = {"username": "user", "password": "Qwerty!234"}
        url = reverse("login")
        response = self.client.post(url, data=credentials_data, format="json")
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_positive(self):
        """
        Проверяет успешный вход пользователя
        Returns: None
        """
        credentials_data = {
            "username": "custom_user",
            "password": "Qwerty!234"
        }
        url = reverse("login")
        response = self.client.post(url, data=credentials_data, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue("tokens" in response.data)

        tokens = response.data["tokens"]

        refresh_url = reverse("token_refresh")
        response = self.client.post(refresh_url, data={"refresh": tokens["refresh"]}, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

