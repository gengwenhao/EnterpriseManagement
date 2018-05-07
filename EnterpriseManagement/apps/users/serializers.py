"""
    用户信息, 注册序列化
"""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import (
    UserProfile,
    Message
)


class UserProfileSerializer(serializers.ModelSerializer):
    """
        UserProfileSerializer
    """

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name', 'gender', 'date_joined', 'last_login', 'email',)


class RegisterSerializer(serializers.ModelSerializer):
    """
        注册序列化
    """
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message='用户已存在')])
    password = serializers.CharField(
        style={'input_type': 'password'},
        label='密码',
        write_only=True
    )

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    new_password = serializers.CharField(required=True)



class MessageSerializer(serializers.ModelSerializer):
    """
        用户留言序列化
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    name = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('content', 'user', 'name', 'id', 'time')

    def get_time(self, instance):
        data_time = str(instance.add_time) \
            .split('.')[0] \
            .split(' ')

        date_time_dict = dict(
            date=data_time[0],
            time=data_time[1],
        )

        return date_time_dict

    def get_name(self, instance):
        return str(instance.user)
