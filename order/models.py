import uuid
from django.db import models

from core.rest.tests.custom_data_generator import generate_random_order_no
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()


class Order(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order_no = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=100, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES)

    def calculate_total_order_price(self):
        total_price = 0
        for order_item in self.order_items.filter():
            total_price += order_item.calculate_price()
        return total_price

    def __str__(self):
        return f"Order no {self.uuid}"

    def generate_order_no(self):
        new_order_no = generate_random_order_no()
        try:
            Order.objects.get(order_no=new_order_no)
            return self.generate_order_no()
        except Order.DoesNotExist:
            self.order_no = new_order_no
            self.save()
            return self.order_no




class OrderItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def calculate_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} from {self.product.shop.name}"
