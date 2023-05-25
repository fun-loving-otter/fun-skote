from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from main.models import DataList

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
