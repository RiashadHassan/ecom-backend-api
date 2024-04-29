from django.shortcuts import get_object_or_404

from rest_framework import permissions
from shop.models import Shop, Member
from common.permissions.helper import CustomGetObjectOr404


class MemberPermission(permissions.BasePermission):

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

        elif member.member_type == "staff":
            return request.method == "GET"

        elif member.member_type == "admin":
            if request.method in ["POST", "PATCH"] and "member_type" in request.data:
                return request.data["member_type"] in ["manager", "staff"]

        elif member.member_type == "manager":
            if request.method in ["POST", "PATCH"] and "member_type" in request.data:
                return request.data["member_type"] in ["staff"]

        return request.method in ["GET", "PUT", "PATCH", "POST"]


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # if request.method == 'POST'


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.method == "GET"
