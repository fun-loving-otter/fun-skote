from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.generics import UpdateAPIView

from main.models import DataList
from main.rest.serializers import DataListSerializer
from main.rest.permissions import IsCreatorPermission



class DataListListView(ListView):
    model = DataList
    template_name = 'main/datalist/datalists.html'
    context_object_name = 'data_lists'
    ordering = ['-last_modified']



class DataListCreateView(LoginRequiredMixin, CreateView):
    model = DataList
    template_name = 'form.html'
    fields = ['name', 'source']
    success_url = reverse_lazy('main:datalist-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)



class DataListUpdateAPIView(UpdateAPIView):
    # permission_classes = [IsCreatorPermission]
    serializer_class = DataListSerializer
    queryset = DataList.objects.all()
    http_method_names = ['patch']
