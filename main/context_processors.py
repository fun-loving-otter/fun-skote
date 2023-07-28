from main.models import UserThrottledActionEntry
from main.mixins import DataPackageCheckerMixin


# TODO: write tests for this
def credits_usage(request):
    user = request.user

    if not user.is_authenticated:
        return {}

    if getattr(user, 'data_package_subscription', None) is not None:
        # View has DataPackageChecker mixin and get_subscription was called
        # Which resulted in assignment of data_package_subscription property
        subscription = user.data_package_subscription

    elif not hasattr(user, 'data_package_subscription'):
        # View does not have DataPackageChecker mixin
        checker = DataPackageCheckerMixin()
        subscription = checker.get_subscription(user=user)

    else:
        return {}

    usage = UserThrottledActionEntry.get_mapped_usage(user, subscription)
    return {
        'CREDITS_USAGE': usage
    }
