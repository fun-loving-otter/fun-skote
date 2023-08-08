from payments.utilities import SubscriptionChecker
from payments.models import Subscription


class DataPackageSubscriptionMiddleware(SubscriptionChecker):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        subscription = self.get_subscription(user=request.user)
        request.user.subscription = subscription

        response = self.get_response(request)
        return response
