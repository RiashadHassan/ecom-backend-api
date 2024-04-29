from django.shortcuts import get_object_or_404

from rest_framework import permissions

from common.permissions.helper import CustomGetObjectOr404
from shop.models import Shop, Member


class ShopPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        shop_uuid = view.kwargs.get("shop_uuid")
        shop = get_object_or_404(Shop, uuid=shop_uuid)

        member = CustomGetObjectOr404.get_object_or_404(
            Member, user=request.user, shop=shop
        )

        if member.member_type == "owner":
            return True

        elif member.member_type == "admin":
            return request.method != "DELETE"

        elif member.member_type in ["manager", "staff"]:
            return request.method == "GET"


class DefaultShopPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # to check if user is a member in a specific shop and noty just any shop
        member = get_object_or_404(Member, user=request.user, last_visited=True)
        if member.member_type == "owner":
            return True

        elif member.member_type in ["admin", "manager"]:
            return request.method != "DELETE"

        elif member.member_type == "staff":
            return request.method == "GET"


class ProductPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        shop_uuid = view.kwargs.get("shop_uuid")
        shop = get_object_or_404(Shop, uuid=shop_uuid)

        # to check if user is a member in a specific shop and noty just any shop
        member = get_object_or_404(Member, user=request.user, shop=shop)
        if member.member_type in ["owner", "admin", "manager"]:
            return True

        elif member.member_type == "staff":
            return request.method == "GET"
