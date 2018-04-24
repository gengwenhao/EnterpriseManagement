import json

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.http import HttpResponse
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from users.filters import UserProfileFilter
from users.models import UserProfile
from users.serializers import UserProfileSerializer, RegisterSerializer, MessageSerializer


class LogoutView(View):
    def get(self, request):
        # success 0 , failed 1
        return_data = {'status': 0}

        logout(request)
        return_data['status'] = 1

        response = HttpResponse(json.dumps(return_data), content_type='application/json')
        return response


class LoginView(View):
    def post(self, request):
        # success 0 , failed 1
        return_data = {'status': 0}

        try:
            info = json.loads(request.body)
            user = authenticate(**info)
        except Exception as e:
            user = None

        if user is not None:
            login(request, user)
            return_data = {'status': 1}

        response = HttpResponse(json.dumps(return_data), content_type='application/json')
        return response


class RegisterViewset(CreateModelMixin,
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


class MessageViewset(CreateModelMixin,
                     viewsets.GenericViewSet):
    """
        用户留言
    """
    serializer_class = MessageSerializer


class UserProfilePagination(PageNumberPagination):
    """
        用户分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class UserProfileViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet,
                         mixins.RetrieveModelMixin):
    """
    list:
        用户列表页
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
