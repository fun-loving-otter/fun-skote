from rest_framework.throttling import BaseThrottle

from main.utilities import Limiter


class LimitedActionThrottle(Limiter, BaseThrottle):
    action_name = None
    action_cost = None

    def allow_request(self, request, view):
        self.view = view
        return super().allow_request(request)


    def get_action_name(self):
        can_get = hasattr(self.view, 'get_action_name')
        if can_get:
            return self.view.get_action_name()
        else:
            return self.view.action_name


    def get_action_cost(self):
        can_get = hasattr(self.view, 'get_action_cost')
        if can_get:
            return self.view.get_action_cost()
        else:
            return self.view.action_cost
