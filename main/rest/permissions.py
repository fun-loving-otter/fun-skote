from rest_framework.permissions import BasePermission

from main.models import PackageSubscription


class IsCreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user



class HasPackagePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        try:
            subscription = user.packagesubscription.subscription
        except PackageSubscription.DoesNotExist:
            return False

        if subscription.status != 'a' or subscription.check_expiration():
            return False

        return True
