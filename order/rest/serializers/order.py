from rest_framework import serializers

from common.helper import DynamicFieldsModelSerializer

from order.models import Order, OrderItem
from product.models import Product, CustomerReview


class OrderItemSerializer(DynamicFieldsModelSerializer):
    product = serializers.UUIDField(source="product.uuid")
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["uuid", "product", "quantity", "price"]

    def get_price(self, obj):
        return obj.calculate_price()


class OrderSerializer(DynamicFieldsModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "uuid",
            "total_amount",
            "order_date",
            "delivery_status",
            "order_items",
        ]


class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["uuid", "total_amount", "delivery_status", "order_date"]


class OrderItemReviewSerializer(serializers.ModelSerializer):
    product = serializers.UUIDField(source="product.uuid", required=False)
    order = serializers.UUIDField(source="order.uuid", required=False)
    rating = serializers.IntegerField(required=False)
    review = serializers.CharField(required=False)

    class Meta:
        model = OrderItem
        fields = ["uuid", "order", "product", "quantity", "rating", "review"]
        read_only_fields = ["uuid", "order", "product", "quantity"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context["request"].user
        try:
            rating_data = CustomerReview.objects.get(
                product=instance.product, user=user
            )
            data["rating"] = rating_data.rating
            data["review"] = rating_data.review
        except CustomerReview.DoesNotExist:
            data["rating"] = None
            data["review"] = None
        return data

    def update(self, instance, validated_data):

        if instance.order.delivery_status != "Delivered":
            raise serializers.ValidationError("Order must be delivered first")

        rating_data = validated_data.pop("rating", None)
        review_data = validated_data.pop("review", None)

        if rating_data is not None:
            instance.product.ratings.update_or_create(
                defaults={"rating": rating_data}, user=self.context["request"].user
            )

        if review_data is not None:
            instance.product.ratings.update_or_create(
                defaults={"review": review_data}, user=self.context["request"].user
            )

        return instance

    def validate(self, data):
        if "rating" in data and data["rating"] not in [1, 2, 3, 4, 5]:
            raise serializers.ValidationError("Rating must range from 1 to 5")
        return data
