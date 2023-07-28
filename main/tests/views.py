from rest_framework.views import APIView
from rest_framework.response import Response

from main.rest.throttles import LimitedActionThrottle
from main.mixins import DataPackageCheckerMixin
from main.consts import action_names

static_rate = 10


class LimitedActionView(DataPackageCheckerMixin, APIView):
    action_name = action_names.ACTION
    action_cost = 1
    throttle_classes = [LimitedActionThrottle]

    def get(self, request, format=None):
        return Response({'message': 'GET request allowed'})




class LimitedActionView2(DataPackageCheckerMixin, APIView):
    action_name = action_names.EXPORT
    action_cost = 1
    throttle_classes = [LimitedActionThrottle]

    def get(self, request, format=None):
        return Response({'message': 'GET request allowed'})
