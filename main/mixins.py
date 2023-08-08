from django.contrib.auth.mixins import UserPassesTestMixin

from payments.mixins import SubscriptionRequiredMixin, SubscriptionCheckerMixin

from main.utilities import Limiter


class DataPackageCheckerMixin(SubscriptionCheckerMixin):
    '''
    This mixin assumes that DataPackageSubscriptionMiddleware
    was applied, so call to the original get_subscription
    is not required
    '''
    def get_subscription(self, user, **kwargs):
        return user.subscription



class DataPackageRequiredMixin(SubscriptionRequiredMixin):
    '''
    This mixin assumes that DataPackageSubscriptionMiddleware
    was applied, so call to the original get_subscription
    is not required
    '''

    def get_subscription(self, user, **kwargs):
        return user.subscription



class LimitedActionMixin(Limiter, UserPassesTestMixin):
    def test_func(self):
        return self.allow_request(self.request)
