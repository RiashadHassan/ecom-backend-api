from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from core.rest.tests import payloads, urlhelpers

from cart.models import Cart

User = get_user_model()


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_payload = payloads.user_create_payload()

        self.user = User.objects.create_user(
            phone_number=self.user_payload["phone_number"],
            password=self.user_payload["password"],
            username=self.user_payload["username"],
        )

        login_data = {
            "phone_number": self.user_payload["phone_number"],
            "password": self.user_payload["password"],
        }

        self.user_login = self.client.post(urlhelpers.get_token_url(), login_data)
        self.assertEqual(self.user_login.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer" + self.user_login.data["access"]
        )
        self.client.force_authenticate(user=self.user)
