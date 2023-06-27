from django.urls import reverse_lazy

from payments.mixins import SubscriptionRequiredMixin
from payments.models import Subscription


class DataPackageRequiredMixin(SubscriptionRequiredMixin):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)
    subscription_does_not_exist_url = reverse_lazy('main:buy-package')
