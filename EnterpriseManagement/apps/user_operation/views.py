from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (viewsets,
                            mixins)
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import Board
from user_operation.serializers import BoardSerializers
from users.models import UserProfile


class BoardPagination(PageNumberPagination):
    """
        留言分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class BoardViewset(CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin):
    """
        用户留言
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    serializer_class = BoardSerializers
    pagination_class = BoardPagination

    # filter_backends = (
    #     DjangoFilterBackend,
    # )
    # filter_class = BoardFilter

    def get_queryset(self):
        user_id = self.request.user.id

        try:
            user_orgs = UserProfile.objects.get(id=user_id).user_orgs.all()
        except UserProfile.DoesNotExist as e:
            user_orgs = []

        queryset_ = Board.objects.filter(Q(type=0) |
                                         Q(type=1, target_id__in=user_orgs) |
                                         Q(type=2, target_id=user_id)).distinct()
        return queryset_
