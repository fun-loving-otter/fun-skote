from main.models import UserThrottledActionEntry
from payments.utilities import SubscriptionChecker
from payments.models import Subscription


class AttachUsageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            usage = UserThrottledActionEntry.get_mapped_usage(user)
            request.usage = usage

            subscription_checker = SubscriptionChecker()
            subscription_checker.subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)

            request.subscription = subscription_checker.get_subscription(user)

        response = self.get_response(request)
        return response
