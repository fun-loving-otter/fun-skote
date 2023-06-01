from django.shortcuts import redirect
from django.urls import reverse

from main.models import PackageSubscription
from payments.consts import subscription_status



class PackageRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # Admins
        if user.is_superuser or user.is_staff:
            return super().dispatch(request, *args, **kwargs)


        subscription = self.get_subscription(user)


        # User should choose package
        if not user.is_authenticated or not subscription:
            return self.redirect_to_buy_package()


        # User didn't pay for package yet
        if subscription.status != subscription_status.ACTIVE or subscription.check_expiration():
            return self.redirect_to_subscription_init()


        return super().dispatch(request, *args, **kwargs)



    def get_subscription(self, user):
        try:
            return user.packagesubscription.subscription
        except PackageSubscription.DoesNotExist:
            return None



    def redirect_to_buy_package(self):
        return redirect(reverse('main:buy-package'))



    def redirect_to_subscription_init(self):
        return redirect(reverse('subscription-init'))
