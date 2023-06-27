from rest_framework.views import APIView
from rest_framework.response import Response

from main.rest.throttles import LimitedActionThrottle

static_rate = 10


class LimitedActionView(APIView):
    action_name = 'Action1'
    action_cost = 1
    throttle_classes = [LimitedActionThrottle]

    def get(self, request, format=None):
        return Response({'message': 'GET request allowed'})




class LimitedActionView2(APIView):
    action_name = 'Action2'
    action_cost = 1
    throttle_classes = [LimitedActionThrottle]

    def get(self, request, format=None):
        return Response({'message': 'GET request allowed'})
