from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import UserProfile, Message


class UserProfileSerializer(serializers.ModelSerializer):
    """
        UserProfileSerializer
    """

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name', 'gender', 'date_joined', 'last_login', 'email',)


class RegisterSerializer(serializers.ModelSerializer):
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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'user')
