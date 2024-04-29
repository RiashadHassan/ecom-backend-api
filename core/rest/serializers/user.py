from django.contrib.auth import get_user_model

from rest_framework import serializers

from common.helper import DynamicFieldsModelSerializer


from shop.rest.serializers.member import ManageMemberSerializer

from cart.models import Cart


class UserSerializer(DynamicFieldsModelSerializer):  # shop info not found
    associated_shops = ManageMemberSerializer(
        many=True,
        fields=("member_type", "shop_name"),
        source="member_set",
        read_only=True,
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["uuid", "phone_number", "username", "password", "associated_shops"]
        read_only_fields = ["uuid"]

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.username = validated_data.get("username", instance.username)
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)  # Hash the password
        instance.save()
        return instance

    def validate(self, data):
        if "password" in data and len(data["password"]) < 5:
            raise serializers.ValidationError("Password must be at least 5 characters")
        return data
