"""
    用户发起的公告, 群发消息,
"""
from django.db import models
from django.utils import timezone

from users.models import UserProfile


class Board(models.Model):
    """
        公告
    """
    content = models.TextField(verbose_name='公告内容')
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING,
                             verbose_name='公告发起人')
    type = models.IntegerField(choices=(
        (0, '发给所有人'),
        (1, '发给某个组织'),
        (2, '发给某个人'),
    ), verbose_name='公告类型')
    target_id = models.IntegerField(null=True, blank=True ,verbose_name='收到公告的组织或用户(发给所有人时, 该字段不生效)')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return f'{self.user} {self.content[:50]}'
