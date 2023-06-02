from rest_framework.permissions import BasePermission

from payments.rest.permissions.package import HasSubscriptionPermission
from payments.models import SubscriptionPackage



class IsCreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user



class HasDataPackagePermission(HasSubscriptionPermission):
    package_queryset = SubscriptionPackage.objects.exclude(datapackagebenefits=None)
