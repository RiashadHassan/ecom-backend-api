import json
from rest_framework import status

from common.tests.base_test import BaseTest
from . import payloads, urlhelpers


class UserApiTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.user_payload = payloads.user_create_payload()
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        response = self.client.post(urlhelpers.create_user_url(), self.user_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user(self):
        response = self.client.get(urlhelpers.update_user_url())
        # print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):

        update_payload = payloads.user_create_payload()
        response = self.client.patch(urlhelpers.update_user_url(), update_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        response = self.client.delete(urlhelpers.update_user_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
