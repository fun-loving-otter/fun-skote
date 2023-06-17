import calendar

from django.db.models import Sum
from django.utils import timezone

from main.models import UserThrottledActionEntry



class Limiter:
    action_name = "DefaultAction"
    action_cost = 1

    def get_throttled_action_name(self):
        return self.action_name


    def get_action_cost(self):
        return self.action_cost


    def get_user_rate(self, subscription):
        if subscription is not None:
            return subscription.package.datapackagebenefits.credits
        else:
            return 0


    def allow_request(self, request=None):
        if request is None:
            request = self.request

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        # Assuming subscription was assigned by middleware
        rate = self.get_user_rate(request.subscription)

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
