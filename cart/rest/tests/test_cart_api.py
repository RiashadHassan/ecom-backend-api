import json
from rest_framework import status

from common.tests.base_test import BaseTest

from . import urlhelpers


class CartTest(BaseTest):
    def setUp(self):
        super().setUp()

    def test_user_cart_details(self):

        respone = self.client.get(urlhelpers.get_user_cart())
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        print(json.dumps(respone.data, indent=4))
