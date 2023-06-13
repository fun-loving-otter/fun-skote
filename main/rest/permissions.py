from rest_framework.permissions import BasePermission

from payments.rest.permissions.subscription import HasSubscriptionPermission
from payments.models import Subscription



class IsCreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user



class HasDataPackagePermission(HasSubscriptionPermission):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)
