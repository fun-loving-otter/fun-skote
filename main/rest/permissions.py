from rest_framework.permissions import BasePermission

from main.models import PackageSubscription
from payments.consts import subscription_status



class IsCreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user



class HasPackagePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Admins
        if user.is_superuser or user.is_staff:
            return True

        if not user.is_authenticated:
            return False

        try:
            subscription = user.packagesubscription.subscription
            return subscription.status == subscription_status.ACTIVE and not subscription.check_expiration()
        except PackageSubscription.DoesNotExist:
            return False
