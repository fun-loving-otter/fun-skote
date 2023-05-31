from django.shortcuts import redirect
from django.urls import reverse

from main.models import PackageSubscription



class PackageRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect(reverse('main:buy-package'))

        try:
            subscription = user.packagesubscription.subscription
        except PackageSubscription.DoesNotExist:
            return redirect(reverse('main:buy-package'))

        if subscription.status != 'a' or subscription.check_expiration():
            return redirect(reverse('main:buy-package'))

        return super().dispatch(request, *args, **kwargs)
