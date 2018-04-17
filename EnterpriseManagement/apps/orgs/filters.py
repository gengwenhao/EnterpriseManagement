import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet

from orgs.models import OrgProfile


class OrgsFilter(FilterSet):
    """
        机构过滤类
    """
    min_add_time = django_filters.NumberFilter(name="add_time", lookup_expr='gte')
    max_add_time = django_filters.NumberFilter(name="add_time", lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        """
            根据id查询机构和其子机构
        """
        queryset = queryset.model.objects.filter(
            Q(id=value) |
            Q(parent_id=value) |
            Q(parent__parent_id=value) |
            Q(parent__parent__parent_id=value)
        )

        return queryset

    class Meta:
        model = OrgProfile
        fields = ['add_time', 'code', 'name']
