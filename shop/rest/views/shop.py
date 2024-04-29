from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter

from product.models import Inventory

from common.permissions.shop import *
from common.pagination.shop import ShopListPagination

from shop.models import Shop, Member
from shop.rest.serializers.shop import (
    PublicShopSerializer,
    PrivateShopSerializer,
    ListShopSerializer,
)

"""Public Views"""


class ShopListCreateView(ListCreateAPIView):
    serializer_class = PublicShopSerializer
    queryset = Shop.objects.filter()
    filter_backends = [SearchFilter]
    search_fields = ["name", "location"]

    authentication_classes = [JWTAuthentication]
    pagination_class = ShopListPagination

    def perform_create(self, serializer):
        shop = serializer.save()

        user = self.request.user
        all_memberships = Member.objects.filter(user=user)
        all_memberships.update(last_visited=False)

        Member.objects.create(
            shop=shop, user=user, member_type="owner", last_visited=True
        )


class RetrieveShopView(RetrieveAPIView):
    serializer_class = PublicShopSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        shop_slug = self.kwargs.get("shop_slug")
        shop = get_object_or_404(Shop, slug=shop_slug)
        return shop


"""Private Views"""


class ShopView(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateShopSerializer
    queryset = Shop.objects.filter()
    permission_classes = [DefaultShopPermission]

    def get_object(self):
        member = Member.objects.filter(user=self.request.user, last_visited=True)
        if member:
            return member.shop
        return None


class ListShopView(ListAPIView):
    serializer_class = ListShopSerializer
    permission_classes = [DefaultShopPermission]

    def get_queryset(self):
        user = self.request.user
        return Shop.objects.filter(members__user=user)


class ManageShopView(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateShopSerializer
    queryset = Shop.objects.filter()
    permission_classes = [ShopPermission]

    def get_object(self):
        shop_uuid = self.kwargs.get("shop_uuid")
        shop = get_object_or_404(Shop, uuid=shop_uuid)

        all_memberships = Member.objects.filter(user=self.request.user)
        all_memberships.update(last_visited=False)

        this_membership = Member.objects.get(shop=shop, user=self.request.user)

        this_membership.last_visited = True
        this_membership.save()
        return shop
