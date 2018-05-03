from django.urls import path

from api.views import UserInfo
from api.views import OrgInfo

app_name = 'api'

urlpatterns = [
    # 主页api
    path('userinfo/', UserInfo.as_view(), name='userinfo'),
    path('orginfo/', OrgInfo.as_view(), name='orginfo'),
]
