from django.shortcuts import get_object_or_404
from django.core.management.base import BaseCommand

from shop.models import Shop

from product.models import Product, ProductInventory
from product.rest.tests.payloads import product_create_payload


class Command(BaseCommand):
    help = "Create a certain amount of new users"

    def add_arguments(self, parser):
        parser.add_argument("shop_slug", type=str)
        parser.add_argument("number_of_products", type=int)

    def handle(self, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=kwargs["shop_slug"])
        number = kwargs["number_of_products"]

        for i in range(number):
            payload = product_create_payload()
            payload["shop"] = shop.id
            product = Product.objects.create(
                name=payload["name"],
                description=payload["description"],
                shop=shop,
                price=payload["price"],
            )
            inventory, created = ProductInventory.objects.get_or_create(
                product=product, inventory=shop.inventory
            )
            inventory.quantity = payload["write_quantity"]
            inventory.save()

            print(product.name)
            print(product.description)
            print(product.price)
            print(product.productinventory.quantity)
