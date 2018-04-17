from django.urls import path

from api.views import UserInfo
from api.views import UpdateUserPassword
from api.views import GoodsList
from api.views import OrgInfo
from users.views import LoginView, LogoutView

app_name = 'api'

urlpatterns = [
    # 主页api
    path('userinfo/', UserInfo.as_view(), name='userinfo'),
    path('orginfo/', OrgInfo.as_view(), name='orginfo'),
    path('update-userpassword/', UpdateUserPassword.as_view(), name='update-userpassword'),
    path('goods-list/', GoodsList.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
