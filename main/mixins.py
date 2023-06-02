from payments.mixins import SubscriptionRequiredMixin
from payments.models import SubscriptionPackage

class DataPackageRequiredMixin(SubscriptionRequiredMixin):
    package_queryset = SubscriptionPackage.objects.exclude(datapackagebenefits=None)
