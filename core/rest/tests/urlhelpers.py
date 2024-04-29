from django.urls import reverse


def create_user_url():
    return reverse("user-list")


def get_token_url():
    return reverse("token_obtain_pair")


def update_user_url():
    return reverse("user-details")
