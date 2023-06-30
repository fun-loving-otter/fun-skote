from payments.rest.permissions.subscription import HasSubscriptionPermission
from payments.models import Subscription


class HasDataPackagePermission(HasSubscriptionPermission):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)
