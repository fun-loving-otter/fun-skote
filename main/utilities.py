import calendar

from django.db.models import Sum
from django.utils import timezone

from main.models import UserThrottledActionEntry



class Limiter:
    '''
    Usage of this class requires implementation of get_user_subscription
    '''

    def allow_request(self, request, action, action_cost):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        range_start, range_end = self.get_action_date_range()
        rate = self.get_user_rate(request, action)

        # Count the number of requests made by the user in the current month
        action_count = UserThrottledActionEntry.objects.filter(
            user=request.user,
            timestamp__gte=range_start,
            timestamp__lt=range_end,
            action=action
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Check if the request count exceeds the monthly limit
        if action_count + action_cost <= rate:
            UserThrottledActionEntry.objects.create(
                user=request.user,
                timestamp=timezone.now(),
                action=action,
                amount=action_cost
            )
            return True

        else:
            return False


    def get_action_date_range(self):
        # Calculate the current month's start date and end date
        now = timezone.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate the last day of the current month
        _, month_days = calendar.monthrange(current_month_start.year, current_month_start.month)

        # Calculate the start of the next month
        next_month_start = (current_month_start + timezone.timedelta(days=month_days))

        return current_month_start, next_month_start


    def get_user_rate(self, request, action):
        subscription = self.get_user_subscription(request)

        if subscription is not None:
            return subscription.package.datapackagebenefits.get_credits_for_action(action)
        else:
            return 0


    def get_user_subscription(self, request):
        raise NotImplementedError('get_user_subscription is not implemented')
