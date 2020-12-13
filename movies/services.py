"""
The supplementary functions
"""

from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Movie


def get_client_ip(request):
    "Get client's ip from request"
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    "The supplementary filter class for MovieFilter"
    pass


class MovieFilter(filters.FilterSet):
    "The filter for the movies"
    genres = CharFilterInFilter(field_name="genres__name", lookup_expr="in")
    year = filters.RangeFilter()
    
    class Meta:
        model = Movie
        fields = ('genres', 'year',)


class PaginationMovies(PageNumberPagination):
    "Pagination settings for the movie lists"
    page_size = 1
    max_page_size = 2
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'results': data,
        })
