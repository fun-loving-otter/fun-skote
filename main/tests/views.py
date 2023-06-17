from rest_framework.views import APIView
from rest_framework.response import Response

from main.mixins import LimitedActionMixin

static_rate = 10


class LimitedActionView(LimitedActionMixin, APIView):
    action_name = 'Action1'

    def get(self, request, format=None):
        return Response({'message': 'GET request allowed'})




class LimitedActionView2(LimitedActionMixin, APIView):
    action_name = 'Action2'

    def get(self, request, format=None):
        return Response({'message': 'GET request allowed'})
