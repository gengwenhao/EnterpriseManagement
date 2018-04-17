from rest_framework import serializers

from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
        UserProfileSerializer
    """

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name', 'gender', 'date_joined', 'last_login', 'email',)
