from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from order.models import Order, OrderItem
from order.rest.serializers.order import (
    OrderSerializer,
    OrderItemSerializer,
    OrderItemReviewSerializer,
)


class OrderListAPIView(ListAPIView):

    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        return orders


class OrderItemListAPIView(ListAPIView):
    serializer_class = OrderItemSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        order_uuid = self.kwargs.get("order_uuid")
        print(order_uuid)
        order = get_object_or_404(Order, uuid=order_uuid)
        order_items = OrderItem.objects.filter(
            order__user=self.request.user, order=order
        )
        return order_items


class OrderItemManageView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemReviewSerializer
    queryset = OrderItem.objects.filter()
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        order_item_uuid = self.kwargs.get("order_item_uuid")
        order_item = get_object_or_404(
            OrderItem, uuid=order_item_uuid, order__user=self.request.user
        )

        return order_item
