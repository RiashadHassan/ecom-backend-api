from django.shortcuts import get_object_or_404

from django.db.models.signals import post_save
from django.dispatch import receiver


from order.models import OrderItem
from .models import Inventory, ProductInventory
from shop.models import Shop


@receiver(post_save, sender=OrderItem)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        product_inventory = get_object_or_404(
            ProductInventory, product=instance.product
        )
        product_inventory.quantity = product_inventory.quantity - instance.quantity
        product_inventory.save()


@receiver(post_save, sender=Shop)
def create_shop_inventory(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(shop=instance)
