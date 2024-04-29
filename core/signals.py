from django.db.models import Avg
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from product.models import CustomerReview

User = get_user_model()


@receiver(pre_delete, sender=User)
def data_to_update_average_rating(sender, instance, **kwargs):
    reviews = CustomerReview.objects.filter(user=instance)
    if reviews:
        instance._related_products = [review.product for review in reviews]


@receiver(post_delete, sender=User)
def update_average_rating(sender, instance, **kwargs):
    for product in instance._related_products:
        ratings = CustomerReview.objects.filter(product=product)
        if ratings.exists():
            product.average_rating = ratings.aggregate(Avg("rating"))["rating__avg"]
        else:
            product.average_rating = None
        product.save()
