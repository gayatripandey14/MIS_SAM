from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from collections import OrderedDict
from rest_framework import  status


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    page_size = 10
    envelope = True

    def paginate_queryset(self, queryset, request, view=None):
        paginated_qs = super().paginate_queryset(queryset, request, view)
        self.get_first_link(
            int(
                request.query_params.get(self.page_size_query_param,
                                         self.page_size)))
        self.get_last_link(
            int(
                request.query_params.get(self.page_size_query_param,
                                         self.page_size)))
        return paginated_qs

    def get_paginated_response(self, data, count):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        return Response(OrderedDict([('total Count', count),
                                     ('first', self.first_page),
                                     ('next', next_url),
                                     ('previous', previous_url),
                                     ('last', self.last_page),
                                     ('records', data)]),
                        status=status.HTTP_200_OK)

    def get_first_link(self, page_size):
        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.page_size_query_param, page_size)
        self.first_page = replace_query_param(url, self.page_query_param, 1)

    def get_last_link(self, page_size):
        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.page_size_query_param, page_size)
        self.last_page = replace_query_param(url, self.page_query_param,
                                             self.page.paginator.num_pages)