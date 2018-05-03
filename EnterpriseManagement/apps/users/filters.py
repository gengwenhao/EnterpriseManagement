import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet

from users.models import UserProfile


class UserProfileFilter(FilterSet):
    """
        用户过滤类
    """
    min_date_joined = django_filters.NumberFilter(name="date_joined", lookup_expr='gte')
    max_date_joined = django_filters.NumberFilter(name="date_joined", lookup_expr='lte')
    user_orgs = django_filters.NumberFilter(method='user_org_id_filter')

    def user_org_id_filter(self, queryset, name, value):
        result = queryset.filter(Q(user_orgs=value) |
                                 Q(user_orgs__parent=value) |
                                 Q(user_orgs__parent__parent=value) |
                                 Q(user_orgs__parent__parent__parent=value) |
                                 Q(user_orgs__parent__parent__parent__parent=value)).distinct()
        return result

    class Meta:
        model = UserProfile
        fields = ['min_date_joined', 'max_date_joined']
