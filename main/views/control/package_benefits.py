from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy

from payments.models import SubscriptionPackage
from main.models import DataPackageBenefits
from authentication.utilities import AccessRequiredMixin


class PackageWithBenefitsListView(AccessRequiredMixin, ListView):
    model = SubscriptionPackage
    template_name = 'main/control/package/package_list_with_benefits.html'
    context_object_name = 'packages'



class PackageBenefitsUpdateView(UpdateView):
    model = DataPackageBenefits
    template_name = 'control/form.html'
    fields = ['credits']
    success_url = reverse_lazy('control_panel:package-benefits')

    def get_object(self, queryset=None):
        package_pk = self.kwargs.get('package_pk')
        obj, created = DataPackageBenefits.objects.get_or_create(package_id=package_pk)
        return obj
