import json
from django.shortcuts import get_object_or_404
from rest_framework import status

from common.tests.base_test import BaseTest

from order.models import Order, OrderItem
from . import payloads, urlhelpers

from product.models import Product

from product.rest.tests.payloads import product_create_payload
from product.rest.tests.urlhelpers import product_create_url

from shop.models import Shop
from shop.rest.tests.payloads import shop_create_payload
from shop.rest.tests.urlhelpers import me_shop_list_create_url


class CartTest(BaseTest):
    def setUp(self):
        super().setUp()

        shop_creation = self.client.post(
            me_shop_list_create_url(), shop_create_payload()
        )
        self.shop = get_object_or_404(Shop, uuid=shop_creation.data["uuid"])
        product_payload = product_create_payload()

        product_payload["shop"] = self.shop
        product_creation = self.client.post(
            product_create_url(self.shop.uuid), product_payload
        )
        self.product = get_object_or_404(Product, uuid=product_creation.data["uuid"])

    def test_create_cart_items(self):

        payload = payloads.cart_item_create_payload()
        payload["product_uuid"] = self.product.uuid

        response = self.client.post(urlhelpers.get_list_create_cart_items(), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_cart_items(self):
        self.test_create_cart_items()

        response = self.client.get(urlhelpers.get_list_create_cart_items())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(json.dumps(response.data, indent=4, default=float))

    # ORDER TESTS

    def test_order_list(self):
        response = self.client.get(urlhelpers.order_list_url())
        print(json.dumps(response.data, indent=4, default=float))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_create(self):
        self.test_create_cart_items()
        response = self.client.post(urlhelpers.order_create_url())
        print(json.dumps(response.data, indent=4, default=float))
        self.test_order_list()
        order = get_object_or_404(Order, uuid=response.data["order"]["uuid"])
        return order

    def test_order_items_list(self):
        response = self.client.get(urlhelpers.order_items_list_url())
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_items_details(self):
        order = self.test_order_create()
        order_item = OrderItem.objects.filter(order=order).first()
        print(order_item.uuid)

        response = self.client.get(urlhelpers.order_items_detail_url(order_item.uuid))
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_item_review(self):
        order = self.test_order_create()
        order_item = OrderItem.objects.filter(order=order).first()
        response = self.client.patch(
            urlhelpers.order_item_review_url(order_item.uuid),
            payloads.order_item_review_payload(),
        )
        print(json.dumps(response.data, indent=4))
