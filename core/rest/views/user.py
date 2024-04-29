from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from core.models import *

from core.rest.serializers.user import (
    UserSerializer,
)


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    queryset = User.objects.filter()
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return get_object_or_404(User, uuid=self.request.user.uuid)
