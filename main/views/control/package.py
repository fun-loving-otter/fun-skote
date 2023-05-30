from django.views.generic import ListView, UpdateView, CreateView
from django.urls import reverse_lazy

from rest_framework.generics import DestroyAPIView

from main.models import Package
from authentication.utilities import AccessRequiredMixin
from authentication.rest.permissions import HasAccessPermission


class PackageListView(AccessRequiredMixin, ListView):
    model = Package
    template_name = 'main/control/package/package_list.html'
    context_object_name = 'packages'



class PackageUpdateView(AccessRequiredMixin, UpdateView):
    model = Package
    template_name = 'control/form.html'
    fields = ['name', 'credits', 'price']
    success_url = reverse_lazy('control_panel:packages')



class PackageCreateView(AccessRequiredMixin, CreateView):
    model = Package
    template_name = 'control/form.html'
    fields = ['name', 'credits', 'price']
    success_url = reverse_lazy('control_panel:packages')




class PackageDestroyAPIView(DestroyAPIView):
    queryset = Package.objects.all()
    permission_classes = [HasAccessPermission]
