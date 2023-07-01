from payments.mixins import SubscriptionRequiredMixin
from payments.models import Subscription


class DataPackageRequiredMixin(SubscriptionRequiredMixin):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)
