from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from shop.models import Shop, Member
from rest_framework import serializers

from common.helper import DynamicFieldsModelSerializer

User = get_user_model()


class ListCreateMemberSerializer(DynamicFieldsModelSerializer):
    user_uuid = serializers.UUIDField(write_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Member
        fields = ["uuid", "member_type", "user_uuid", "username"]
        read_only_fields = ["uuid"]

    def create(self, validated_data):
        user_uuid = validated_data.pop("user_uuid")
        user = get_object_or_404(User, uuid=user_uuid)

        member = Member.objects.create(user=user, **validated_data)
        return member


class ManageMemberSerializer(DynamicFieldsModelSerializer):
    shop_name = serializers.CharField(source="shop.name")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Member
        fields = ["uuid", "shop_name", "username", "member_type"]
        read_only_fields = ["uuid"]


8
