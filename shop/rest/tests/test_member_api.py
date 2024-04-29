from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
import json

from common.tests.base_test import BaseTest
from shop.models import Shop, Member
from . import payloads, urlhelpers
from core.rest.tests.payloads import user_create_payload

User = get_user_model()


class MemberTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        shop_creation = self.client.post(
            urlhelpers.me_shop_list_create_url(), payloads.shop_create_payload()
        )
        self.shop = get_object_or_404(Shop, uuid=shop_creation.data["uuid"])

    def test_list_member(self):
        response = self.client.get(urlhelpers.member_list_create_url(self.shop.uuid))
        # print (json.dumps(response.data, indent=4))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_member(self):
        new_user = User.objects.create(
            phone_number=user_create_payload()["phone_number"],
            password=user_create_payload()["password"],
            username=user_create_payload()["username"],
        )
        new_user_uuid = new_user.uuid

        payload = payloads.member_create_payload()
        payload["user_uuid"] = new_user_uuid
        payload["member_type"] = "admin"

        response = self.client.post(
            urlhelpers.member_list_create_url(self.shop.uuid), payload
        )
        # print (json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        member = get_object_or_404(Member, uuid=response.data["uuid"])
        return member

    def test_get_member_details(self):
        member = self.test_create_member()

        response = self.client.get(
            urlhelpers.member_update_url(self.shop.uuid, member.uuid)
        )
        # print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_member(self):
        member = self.test_create_member()
        # print(member.member_type, member.uuid)

        update_payload = payloads.member_update_payload()
        update_payload["member_type"] = "manager"
        response = self.client.patch(
            urlhelpers.member_update_url(self.shop.uuid, member.uuid), update_payload
        )
        # print (json.dumps(response.data, indent=4))

        self.assertEqual(response.data["member_type"], update_payload["member_type"])

    def test_restrict_update_member(self):
        member = self.test_create_member()
        user = get_object_or_404(User, uuid=member.user.uuid)

        self.client.force_authenticate(user=user)

        update_payload = payloads.member_update_payload()
        update_payload["member_type"] = "owner"
        response = self.client.patch(
            urlhelpers.member_update_url(self.shop.uuid, member.uuid), update_payload
        )
        # print (json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_member(self):

        member = self.test_create_member()

        response = self.client.delete(
            urlhelpers.member_update_url(self.shop.uuid, member.uuid)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_restrict_delete_member(self):

        member = self.test_create_member()
        user = get_object_or_404(User, uuid=member.user.uuid)

        self.client.force_authenticate(user=user)

        response = self.client.delete(
            urlhelpers.member_update_url(self.shop.uuid, member.uuid)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
