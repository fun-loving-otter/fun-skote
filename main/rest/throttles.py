from rest_framework.throttling import BaseThrottle

from main.utilities import Limiter


class LimitedActionThrottle(Limiter, BaseThrottle):
    '''
    Usage of this throttle requires usage of DataPackageCheckerMixin on view
    '''
    def allow_request(self, request, view):
        self.view = view

        action = self.get_view_attr(view, 'get_action_name', 'action_name')
        cost = self.get_view_attr(view, 'get_action_cost', 'action_cost', default=1)
        return super().allow_request(request, action, cost)


    def get_view_attr(self, view, getter_name, attr_name, default=None):
        getter = getattr(view, getter_name, None)
        if getter:
            return getter()

        value = getattr(view, attr_name, None)
        if value:
            return value

        if default:
            return default

        raise AttributeError(f"View has no {attr_name} defined")


    def get_user_subscription(self, request):
        return self.view.get_subscription()
