from django.contrib.auth import get_user_model

from rest_framework import status
from common.tests.base_test import BaseTest
from . import payloads, urlhelpers
from shop.models import Shop

User = get_user_model()


class MeShop(BaseTest):
    def setUp(self):
        super().setUp()

        phone_number = self.user_payload["phone_number"]
        self.user = User.objects.get(phone_number=phone_number)
        self.client.force_authenticate(user=self.user)

    def test_get_shop_list(self):
        response = self.client.get(urlhelpers.me_shop_list_create_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_shop(self):
        response = self.client.post(
            urlhelpers.me_shop_list_create_url(), payloads.shop_create_payload()
        )

        shop = Shop.objects.get(uuid=response.data["uuid"])
        member = shop.members.get(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(member.user.uuid, self.user.uuid)
