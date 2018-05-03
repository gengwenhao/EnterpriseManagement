import serializers as serializers
from rest_framework import serializers

from user_operation.models import Board


class BoardSerializers(serializers.ModelSerializer):
    """
        用户留言序列化
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Board
        fields = ('content', 'user', 'type', 'target_id')
