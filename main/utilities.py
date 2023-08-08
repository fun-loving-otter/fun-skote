import calendar

from django.db.models import Sum
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

from main.models import UserThrottledActionEntry


class Limiter:
    '''
    This class assumes that DataPackageSubscriptionMiddleware
    was applied.
    '''
    action_name = None
    action_cost = None

    def allow_request(self, request):
        user = request.user
        self.user = user

        action_name = self.get_action_name()
        action_cost = self.get_action_cost()

        if not user.is_authenticated:
            return False

        if user.is_superuser or user.is_staff:
            return True

        range_start, range_end = self.get_action_date_range()
        rate = self.get_user_rate()

        # Count the number of requests made by the user in the current month
        action_count = UserThrottledActionEntry.objects.filter(
            user=user,
            timestamp__gte=range_start,
            timestamp__lt=range_end,
            action=action_name
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Check if the request count exceeds the monthly limit
        if action_count + action_cost <= rate:
            UserThrottledActionEntry.objects.create(
                user=user,
                timestamp=timezone.now(),
                action=action_name,
                amount=action_cost
            )
            return True

        else:
            return False


    def get_action_name(self):
        if not self.action_name:
            raise ImproperlyConfigured('Provide an action_name.')
        return str(self.action_name)


    def get_action_cost(self):
        if not self.action_cost:
            raise ImproperlyConfigured('Provide an action_cost.')
        return self.action_cost


    def get_action_date_range(self):
        # Calculate the current month's start date and end date
        now = timezone.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate the last day of the current month
        _, month_days = calendar.monthrange(current_month_start.year, current_month_start.month)

        # Calculate the start of the next month
        next_month_start = (current_month_start + timezone.timedelta(days=month_days))

        return current_month_start, next_month_start


    def get_user_rate(self):
        data_package_benefits = self.get_data_package_benefits()
        action_name = self.get_action_name()

        if data_package_benefits is not None:
            return data_package_benefits.get_credits_for_action(action_name)
        else:
            return 0


    def get_data_package_benefits(self):
        if self.user.subscription:
            return self.user.subscription.package.datapackagebenefits
