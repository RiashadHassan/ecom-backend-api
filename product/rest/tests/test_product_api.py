import json
from django.shortcuts import get_object_or_404

from rest_framework import status

from common.tests.base_test import BaseTest

from product.models import Product

from shop.models import Shop
from shop.rest.tests.urlhelpers import me_shop_list_create_url
from shop.rest.tests.payloads import shop_create_payload

from . import payloads, urlhelpers


class ProductTest(BaseTest):
    def setUp(self):
        super().setUp()

        shop_creation = self.client.post(
            me_shop_list_create_url(), shop_create_payload()
        )
        self.shop = get_object_or_404(Shop, uuid=shop_creation.data["uuid"])
        self.product_payload = payloads.product_create_payload()

    def test_create_product(self):
        payload = payloads.product_create_payload()
        payload["shop"] = self.shop
        response = self.client.post(
            urlhelpers.product_create_url(self.shop.uuid), payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # print(json.dumps(response.data, indent=4))
        product = Product.objects.get(uuid=response.data["uuid"])
        return product

    def test_list_products(self):

        response = self.client.get(urlhelpers.product_create_url(self.shop.uuid))
        # print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        product = self.test_create_product()

        updated_payload = payloads.product_update_payload()

        response = self.client.patch(
            urlhelpers.product_update_url(self.shop.uuid, product.uuid),
            data=json.dumps(updated_payload),
            content_type="application/json",
        )

        self.assertEqual(response.data["price"], updated_payload["price"])
        self.assertEqual(response.data["description"], updated_payload["description"])
        self.assertEqual(response.data["quantity"], updated_payload["write_quantity"])
        # print(json.dumps(response.data, indent=4))

    def test_delete_product(self):
        product = self.test_create_product()

        response = self.client.delete(
            urlhelpers.product_update_url(self.shop.uuid, product.uuid)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
