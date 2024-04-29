from django.shortcuts import get_object_or_404

from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from common.permissions.member import MemberPermission

from shop.models import Shop, Member
from shop.rest.serializers.member import (
    ListCreateMemberSerializer,
    ManageMemberSerializer,
)


class ShopMemberListCreateView(ListCreateAPIView):
    serializer_class = ListCreateMemberSerializer
    permission_classes = [MemberPermission]

    def get_queryset(self):
        shop_uuid = self.kwargs.get("shop_uuid")
        shop = get_object_or_404(Shop, uuid=shop_uuid)

        members = Member.objects.filter(shop=shop)
        if not members:
            raise NotFound(detail="This shop does not have any members")

        return members

    def perform_create(self, serializer):
        shop_uuid = self.kwargs.get("shop_uuid")
        shop = get_object_or_404(Shop, uuid=shop_uuid)
        serializer.save(shop=shop)


class ManageShopMemberView(RetrieveUpdateDestroyAPIView):
    serializer_class = ManageMemberSerializer
    queryset = Member.objects.filter()
    permission_classes = [MemberPermission]

    def get_object(self):
        member_uuid = self.kwargs.get("member_uuid", None)
        member = get_object_or_404(Member, uuid=member_uuid)

        return member
