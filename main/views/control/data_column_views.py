# TODO: write tests for this
from django.views.generic import ListView

from rest_framework.generics import UpdateAPIView

from main.models import DataColumnVisibility
from main.rest.serializers import DataColumnVisibilitySerializer
from control_panel.rest.permissions import HasAccessPermission
from control_panel.mixins import AccessRequiredMixin


class DataColumnVisibilityListView(AccessRequiredMixin, ListView):
    model = DataColumnVisibility
    template_name = 'main/control/data/data_column_visibility_list.html'



class DataColumnVisibilityUpdateAPIView(UpdateAPIView):
    queryset = DataColumnVisibility.objects.all()
    serializer_class = DataColumnVisibilitySerializer
    permission_classes = [HasAccessPermission]
