import json

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.http import HttpResponse
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from users.filters import UserProfileFilter
from users.models import UserProfile
from users.serializers import UserProfileSerializer


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


class UserProfilePagination(PageNumberPagination):
    """
        用户分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class UserProfileViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
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
