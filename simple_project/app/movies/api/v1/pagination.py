from math import ceil

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


PAGE_SIZE = 50
MAX_PAGE_SIZE = 100

class FilmWorkPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        total_pages = ceil(self.page.paginator.count / self.page_size)

        return Response({
            'count': self.page.paginator.count,
            'total_pages': total_pages,
            'prev': (
                self.page.previous_page_number() if self.page.has_previous() else None
            ),
            'next': (
                self.page.next_page_number() if self.page.has_next() else None
            ),
            'results': data
        })
