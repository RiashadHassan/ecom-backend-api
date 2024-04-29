from rest_framework import serializers

from common.helper import DynamicFieldsModelSerializer

from product.models import Image


class ImageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Image
        fields = ["uuid", "image"]
