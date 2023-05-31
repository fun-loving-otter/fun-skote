import csv
import xlwt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.generics import UpdateAPIView, DestroyAPIView

from main.models import DataList, Data
from main.rest.serializers import DataListSerializer
from main.rest.permissions import IsCreatorPermission
from main.mixins import PackageRequiredMixin



class DataListListView(PackageRequiredMixin, ListView):
    model = DataList
    template_name = 'main/datalist/datalists.html'
    context_object_name = 'data_lists'
    ordering = ['-last_modified']



class DataListCreateView(PackageRequiredMixin, LoginRequiredMixin, CreateView):
    model = DataList
    template_name = 'form.html'
    fields = ['name', 'source']
    success_url = reverse_lazy('main:datalist-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)





@login_required
def export_datalist_csv(request, pk):
    try:
        data_list = DataList.objects.get(pk=pk, creator=request.user)
    except DataList.DoesNotExist:
        # Handle case when DataList doesn't exist or user is not the creator
        return HttpResponse(status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="data_list_{pk}.csv"'

    writer = csv.writer(response)

    # Write headers
    header_fields = Data._header_field_mapping.keys()
    writer.writerow(header_fields)

    data_objects = data_list.data.all()

    field_names = Data._header_field_mapping.values()

    for data_object in data_objects:
        row = [getattr(data_object, field) for field in field_names]
        writer.writerow(row)

    return response



@login_required
def export_datalist_xls(request, pk):
    try:
        data_list = DataList.objects.get(pk=pk, creator=request.user)
    except DataList.DoesNotExist:
        # Handle case when DataList doesn't exist or user is not the creator
        return HttpResponse(status=403)


    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="datalist_{pk}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('DataList')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = Data._header_field_mapping.keys()
    field_names = Data._header_field_mapping.values()

    for col_num, column in enumerate(columns):
        ws.write(row_num, col_num, column, font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    data_objects = data_list.data.all()
    for data_obj in data_objects:
        row_num += 1
        for col_num, field_name in enumerate(field_names):
            field_value = getattr(data_obj, field_name)
            ws.write(row_num, col_num, field_value, font_style)

    wb.save(response)
    return response



# ============= API VIEWS =============

class DataListUpdateAPIView(UpdateAPIView):
    permission_classes = [IsCreatorPermission]
    serializer_class = DataListSerializer
    queryset = DataList.objects.all()
    http_method_names = ['patch']



class DataListDestroyAPIView(DestroyAPIView):
    permission_classes = [IsCreatorPermission]
    serializer_class = DataListSerializer
    queryset = DataList.objects.all()
