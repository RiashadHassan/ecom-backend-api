import json
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from common.helper import DynamicFieldsModelSerializer

from product.models import Product, Image, Inventory, ProductInventory
from product.rest.serializers.image import ImageSerializer

"""Public Product Serializers"""


class ProductSerializer(DynamicFieldsModelSerializer):
    images = ImageSerializer(many=True, source="image_set", required=False)

    class Meta:
        model = Product
        fields = [
            "uuid",
            "slug",
            "name",
            "description",
            "price",
            "average_rating",
            "profile_image",
            "average_rating",
            "images",
        ]


"""Private Product Serializers"""


class ListCreateProductSerializer(DynamicFieldsModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    quantity = serializers.IntegerField(
        source="productinventory.quantity", read_only=True
    )
    write_quantity = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Product
        fields = [
            "uuid",
            "name",
            "description",
            "price",
            "profile_image",
            "images",
            "quantity",
            "write_quantity",
        ]

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        quantity = validated_data.pop("write_quantity")

        product = Product.objects.create(**validated_data)
        shop = product.shop

        if quantity is not None:
            shop_inventory, _ = Inventory.objects.get_or_create(shop=shop)
            ProductInventory.objects.create(
                inventory=shop_inventory, product=product, quantity=quantity
            )
            print(shop_inventory)

        else:
            raise serializers.ValidationError("A quantity must be specified")

        for image in images:
            Image.objects.create(product=product, image=image)

        return product


class ManageProductSerializer(DynamicFieldsModelSerializer):
    quantity = serializers.IntegerField(
        source="productinventory.quantity", read_only=True
    )
    images = ImageSerializer(many=True, source="image_set", read_only=True)
    write_quantity = serializers.IntegerField(write_only=True, required=False)
    image = serializers.ListField(
        child=VersatileImageFieldSerializer(sizes="product_images"),
        write_only=True,
        required=False,
    )

    delete_image_uuid = serializers.CharField(write_only=True, required=False)
    update_image_uuid = serializers.CharField(write_only=True, required=False)
    update_image = VersatileImageFieldSerializer(
        sizes="product_images", write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "uuid",
            "slug",
            "name",
            "description",
            "profile_image",
            "price",
            "average_rating",
            "quantity",
            "images",
            "write_quantity",
            "image",
            "delete_image_uuid",
            "update_image_uuid",
            "update_image",
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.profile_image = validated_data.get(
            "profile_image", instance.profile_image
        )
        instance.price = validated_data.get("price", instance.price)
        instance.save()

        quantity = validated_data.get("write_quantity")
        if quantity is not None:
            product_inventory = get_object_or_404(ProductInventory, product=instance)
            product_inventory.quantity = quantity
            product_inventory.save()

        images_data = validated_data.pop("image", [])

        for image_data in images_data:
            Image.objects.create(image=image_data, product=instance)

        delete_image_uuid = validated_data.get("delete_image_uuid", None)

        if delete_image_uuid:
            image_to_delete = get_object_or_404(Image, uuid=delete_image_uuid)
            image_to_delete.delete()

        update_image_uuid = validated_data.get("update_image_uuid", None)
        update_image = validated_data.pop("update_image", None)

        if update_image_uuid and update_image:
            image_to_update = get_object_or_404(Image, uuid=update_image_uuid)
            image_to_update.image = update_image
            image_to_update.save()

        return instance
