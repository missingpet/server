from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class AnnouncementPagination(PageNumberPagination):
    """Custom pagination class."""

    page_size = 6

    def get_next_page_number(self):
        return self.page.next_page_number() if self.page.has_next() else None

    def get_previous_page_number(self):
        return self.page.previous_page_number() if self.page.has_previous() else None

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next_page_number": self.get_next_page_number(),
                "previous_page_number": self.get_previous_page_number(),
                "results": data,
            }
        )
