
from django.urls import reverse_lazy
from django.http import HttpResponse

from main.utilities import Limiter
from payments.mixins import SubscriptionRequiredMixin
from payments.models import Subscription



class DataPackageRequiredMixin(SubscriptionRequiredMixin):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)
    subscription_does_not_exist_url = reverse_lazy('main:buy-package')



class LimitedActionMixin(Limiter):
    def dispatch(self, request, *args, **kwargs):
        if not self.allow_request():
            return HttpResponse(status=429)

        return super().dispatch(request, *args, **kwargs)
