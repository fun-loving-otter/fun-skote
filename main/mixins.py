from payments.mixins import SubscriptionRequiredMixin, SubscriptionCheckerMixin
from payments.models import Subscription


class DataPackageCheckerMixin(SubscriptionCheckerMixin):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)

    def get_subscription(self, *args, **kwargs):
        subscription = super().get_subscription(*args, **kwargs)
        if subscription is not None:
            subscription.user.data_package_subscription = subscription
        return subscription



class DataPackageRequiredMixin(SubscriptionRequiredMixin):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)

    def get_subscription(self, *args, **kwargs):
        subscription = super().get_subscription(*args, **kwargs)
        self.request.user.data_package_subscription = subscription
        return subscription
