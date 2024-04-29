from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from order.models import Order, OrderItem
from order.services import order_confirmed
from order.rest.serializers.order import CreateOrderSerializer


class CheckoutView(CreateAPIView):
    serializer_class = CreateOrderSerializer
    authentication_classes = [JWTAuthentication]

    def create(self, request):

        selected_cart_items = request.user.cart.cart_items.filter(selected=True)

        if not selected_cart_items:
            return Response(
                {"message": "No items selected for ordering."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_amount = sum(item.calculate_price() for item in selected_cart_items)

        order = Order.objects.create(
            user=request.user, total_amount=total_amount, delivery_status="Pending"
        )

        order_confirmed.send(sender=self.__class__, order=order)

        for cart_item in selected_cart_items:
            OrderItem.objects.create(
                order=order, product=cart_item.product, quantity=cart_item.quantity
            )
            cart_item.delete()
        order_serializer = CreateOrderSerializer(order)
        return Response(
            {"message": "Order placed successfully.", "order": order_serializer.data},
            status=status.HTTP_201_CREATED,
        )
