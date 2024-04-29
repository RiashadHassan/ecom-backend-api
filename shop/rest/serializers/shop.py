from django.contrib.auth import get_user_model
from common.helper import DynamicFieldsModelSerializer

from shop.models import Shop, Member
from rest_framework import serializers
from shop.rest.serializers.member import ManageMemberSerializer
from product.rest.serializers.product import ProductSerializer

User = get_user_model()


"""Public Serializers"""


class PublicShopSerializer(DynamicFieldsModelSerializer):
    products = ProductSerializer(source="product_set", many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ["uuid", "slug", "name", "location", "products"]
        read_only_fields = ["uuid"]


"""Private Serializers"""


class ListShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ["uuid", "name"]


class PrivateShopSerializer(DynamicFieldsModelSerializer):
    members = ManageMemberSerializer(
        many=True,
        read_only=True,
        fields=("uuid", "user_uuid", "username", "member_type"),
    )
    products = ProductSerializer(source="product_set", many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ["uuid", "name", "location", "members", "products"]
        read_only_fields = ["uuid", "members", "products"]
