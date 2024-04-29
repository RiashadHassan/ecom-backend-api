import uuid
from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model


from versatileimagefield.fields import VersatileImageField
from autoslug import AutoSlugField

from shop.models import Shop

User = get_user_model()


class Product(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from="name", unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    profile_image = VersatileImageField(
        blank=True, null=True, upload_to="images/product_profile"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = VersatileImageField(blank=True, null=True, upload_to="images/")

    def __str__(self):
        return f"image of {self.product.name}"


class Inventory(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventory of {self.shop.name}"


class ProductInventory(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} left of {self.product.name}"


class CustomerReview(models.Model):
    RATING_STAR_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.IntegerField(
        choices=RATING_STAR_CHOICES,
    )
    review = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):

        return f"{self.product.name} - {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ratings = CustomerReview.objects.filter(product=self.product)
        if ratings.exists():
            self.product.average_rating = ratings.aggregate(Avg("rating"))[
                "rating__avg"
            ]
        else:
            self.product.average_rating = None
        self.product.save()
