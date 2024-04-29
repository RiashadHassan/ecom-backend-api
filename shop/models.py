import uuid

from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from autoslug import AutoSlugField

User = get_user_model()


class Shop(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Member(models.Model):

    members = (
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("staff", "Staff"),
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    member_type = models.CharField(max_length=50, choices=members)
    last_visited = models.BooleanField(default=False)

    class Meta:
        # so that one user can be associated with only one membership_type of any store
        unique_together = ("shop", "user")

    def __str__(self):
        return f"{self.member_type} at {self.shop} - {self.user.username}"
