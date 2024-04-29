from shop.models import Member


class DefaultShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated:
            shop = self.get_shop(request)
            request.shop = shop
        else:
            return None
        response = self.get_response(request)

        return response

    def get_shop(self, request):
        member = Member.objects.get(user=request.user, last_visited=True)
        if member:
            return member.shop
        return None
