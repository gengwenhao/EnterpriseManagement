"""
    用户相关, 用户列表, 用户注册
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (viewsets,
                            mixins,
                            status)
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import (jwt_encode_handler,
                                            jwt_payload_handler)

from users.filters import UserProfileFilter
from users.models import (UserProfile,
                          Message)
from users.serializers import (UserProfileSerializer,
                               RegisterSerializer,
                               MessageSerializer, ChangePasswordSerializer)


class RegisterViewSet(CreateModelMixin,
                      viewsets.GenericViewSet):
    """
        用户注册
    """
    serializer_class = RegisterSerializer
    queryset = UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["username"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class UserProfilePagination(PageNumberPagination):
    """
        用户分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class MessagePagination(PageNumberPagination):
    """
        留言分页
    """
    page_size = 4
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class MessageViewSet(CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet,
                     mixins.DestroyModelMixin):
    """
        用户留言
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    # permission_classes = (AllowAny,)
    serializer_class = MessageSerializer
    pagination_class = MessagePagination

    # lookup_field = 'user_id'

    def get_queryset(self):
        return Message.objects.filter(user_id=self.request.user)
        # return Message.objects.all()


class UserProfileViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin):
    """
        用户列表
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_class = UserProfileFilter
    search_fields = ('name', 'email',)
    ordering_fields = ('date_joined',)


class ChangePasswordViewSet(viewsets.GenericViewSet,
                            mixins.UpdateModelMixin):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    model = UserProfile
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
