from rest_framework_datatables.pagination import DatatablesPageNumberPagination


class CustomDatatablesPaginator(DatatablesPageNumberPagination):
    page_size = 25  # number of items per page
    max_page_size = 25
    max_page_number = 20  # max number of pages

    def __init__(self, *args, **kwargs):
        self.max_results = self.page_size * self.max_page_number
        super().__init__(*args, **kwargs)


    def paginate_queryset(self, queryset, request, view=None):
        queryset = queryset[:self.page_size * self.max_page_number]
        return super().paginate_queryset(queryset, request, view)


    def get_paginated_response(self, data):
        if self.page.number > self.max_page_number:
            data = []  # return an empty list if page number exceeds max_page_number

        return super().get_paginated_response(data)
