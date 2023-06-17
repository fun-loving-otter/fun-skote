import calendar

from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse

from main.models import UserThrottledActionEntry
from payments.mixins import SubscriptionRequiredMixin
from payments.models import Subscription



class DataPackageRequiredMixin(SubscriptionRequiredMixin):
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)
    subscription_does_not_exist_url = reverse_lazy('main:buy-package')



class LimitedActionMixin(DataPackageRequiredMixin):
    action_name = "DefaultAction"

    def dispatch(self, request, *args, **kwargs):
        self.get_subscription(request.user)

        if not self.allow_request():
            return HttpResponse(status=429)

        return super().dispatch(request, *args, **kwargs)


    def get_throttled_action_name(self):
        return self.action_name


    def get_action_cost(self):
        '''Used for calculating export since 1 view access can export many rows'''
        return 1


    def get_user_rate(self):
        # Assuming subscription was assigned somewhere already (hopefully)
        credits = self.subscription.package.datapackagebenefits.credits
        return credits


    def allow_request(self):
        request = self.request

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        rate = self.get_user_rate()

        # Calculate the current month's start date and end date
        now = timezone.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate the last day of the current month
        _, month_days = calendar.monthrange(current_month_start.year, current_month_start.month)

        # Calculate the start of the next month
        next_month_start = (current_month_start + timezone.timedelta(days=month_days))

        action = self.get_throttled_action_name()

        # Count the number of requests made by the user in the current month
        action_count = UserThrottledActionEntry.objects.filter(
            user=request.user,
            timestamp__gte=current_month_start,
            timestamp__lt=next_month_start,
            action=action
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        action_cost = self.get_action_cost()

        # Check if the request count exceeds the monthly limit
        if action_count + action_cost <= rate:
            UserThrottledActionEntry.objects.create(
                user=request.user,
                timestamp=now,
                action=action,
                amount=action_cost
            )
            return True

        else:
            return False
