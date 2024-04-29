from django.shortcuts import get_object_or_404

from rest_framework import serializers

from common.helper import DynamicFieldsModelSerializer

from cart.models import Cart, CartItem
from product.models import Product


class ManageCartItemSerializer(DynamicFieldsModelSerializer):
    product = serializers.UUIDField(source="product.uuid", read_only=True)
    cart_item_total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["uuid", "product", "quantity", "cart_item_total_price", "selected"]

    def get_cart_item_total_price(self, obj):
        return obj.calculate_price()


class ListCreateCartItemSerializer(DynamicFieldsModelSerializer):
    product_slug = serializers.SlugField(source="product.slug", read_only=True)
    cart_item_total_price = serializers.SerializerMethodField()
    selected = serializers.BooleanField(default=True)
    product_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = CartItem
        fields = [
            "uuid",
            "product_uuid",
            "product_slug",
            "quantity",
            "cart_item_total_price",
            "selected",
        ]

    def get_cart_item_total_price(self, obj):
        return obj.calculate_price()

    def create(self, validated_data):
        product_uuid = validated_data.get("product_uuid")
        product = get_object_or_404(Product, uuid=product_uuid)

        cart = self.context["request"].user.cart

        # if CartItem.objects.get(product=product, cart=cart):
        #     raise serializers.ValidationError("Product already exists in cart")

        quantity = validated_data.get("quantity")

        if product.productinventory.quantity < quantity:
            raise serializers.ValidationError("Not enough quantity in stock")

        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity
        )

        return cart_item

    def validate(self, data):
        if "quantity" in data and data["quantity"] < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return data


class CartSerializer(DynamicFieldsModelSerializer):
    cart_items = ManageCartItemSerializer(
        many=True,
        read_only=True,
        fields=("uuid", "product", "quantity", "cart_item_total_price"),
    )
    cart_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["cart_total_price", "cart_items"]
        read_only_fields = ["uuid"]

    def get_cart_total_price(self, obj):
        return obj.calculate_total_cart_price()
