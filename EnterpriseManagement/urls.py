"""EnterpriseManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from orgs.views import OrgProfileViewSet
from user_operation.views import BoardViewSet
from users.views import (
    UserProfileViewSet,
    RegisterViewSet,
    MessageViewSet,
    ChangePasswordViewSet)

router = routers.DefaultRouter()
router.register('org_profile', OrgProfileViewSet, base_name='org_profile')
router.register('user_profile', UserProfileViewSet, base_name='user_profile')
router.register('change_password', ChangePasswordViewSet, base_name='change_password')
router.register('message_profile', MessageViewSet, base_name='message_profile')
router.register('register', RegisterViewSet, base_name='register')
router.register('board', BoardViewSet, base_name='board')

urlpatterns = [
    # admin
    # path('admin/', admin.site.urls),
    path('admin/', xadmin.site.urls),

    path('', TemplateView.as_view(template_name='index.html')),

    # rest-framework
    # path('', include(router.urls)),
    path('login/', obtain_jwt_token),
    path('docs/', include_docs_urls(title='企业会议系统')),
    path('api-auth/', include('rest_framework.urls')),

    # api
    path('api/', include('api.urls', namespace='api'))
]
