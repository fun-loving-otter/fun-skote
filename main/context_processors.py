from main.models import UserThrottledActionEntry
from payments.utilities import SubscriptionChecker
from payments.models import Subscription


# TODO: write tests for this
def credits_usage(request):
    user = request.user

    usage = None
    if user.is_authenticated:
        subscription_checker = SubscriptionChecker()
        subscription_checker.subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)
        subscription = subscription_checker.get_subscription(user)

        usage = UserThrottledActionEntry.get_mapped_usage(user, subscription)

    return {
        'CREDITS_USAGE': usage
    }
