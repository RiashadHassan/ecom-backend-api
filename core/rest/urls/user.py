from django.urls import path

from core.rest.views.user import *

urlpatterns = [
    path("/users/onboarding", CreateUserView.as_view(), name="user-list"),
    path("/me", ManageUserView.as_view(), name="user-details"),
]
