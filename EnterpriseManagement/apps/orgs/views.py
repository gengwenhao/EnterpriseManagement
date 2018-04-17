from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from orgs.filters import OrgsFilter
from orgs.models import OrgProfile
from orgs.serializers import OrgProfileSerializer


class OrgProfilePagination(PageNumberPagination):
    """
        机构分页
    """
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class OrgProfileViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    list:
        机构列表页
    """

    queryset = OrgProfile.objects.filter(category_type=1)
    serializer_class = OrgProfileSerializer
    # 分页类
    pagination_class = OrgProfilePagination
    # 过滤引擎
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    # 过滤类
    filter_class = OrgsFilter
    # 搜索字段
    search_fields = ('name',)
    # 排序字段
    ordering_fields = ('code',)
