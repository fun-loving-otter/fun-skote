from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse

from main.utilities import Limiter
from payments.mixins import SubscriptionRequiredMixin
from payments.models import Subscription



class DataPackageRequiredMixin(SubscriptionRequiredMixin):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)
    subscription_does_not_exist_url = reverse_lazy('main:buy-package')



class LimitedActionMixin(Limiter, UserPassesTestMixin):
    def test_func(self):
        return self.allow_request()


    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            return HttpResponse(status=429)
