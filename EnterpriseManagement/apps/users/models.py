from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone

from orgs.models import OrgProfile


class UserType(models.Model):
    """
        用户类型
    """
    name = models.CharField(max_length=150, verbose_name='名称')
    content = models.CharField(max_length=150, verbose_name='用户类型')

    class Meta:
        verbose_name = '用户类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    """
        用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    gender_choices = (
        ('male', '男'),
        ('female', '女'),
    )
    gender = models.CharField(max_length=6, choices=gender_choices, default='male', verbose_name='性别')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮箱')
    user_type = models.ForeignKey(UserType, null=True, blank=True, on_delete=models.CASCADE, verbose_name='用户权限')
    user_orgs = models.ManyToManyField(OrgProfile, verbose_name='用户所属机构')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name or self.username

    @classmethod
    def new_users_today(cls):
        return cls.objects.filter(date_joined__day=datetime.today().day)


class VerifyCode(models.Model):
    """
        短信验证码
    """
    code = models.CharField(max_length=25, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class Message(models.Model):
    """
        用户留言
    """
    content = models.CharField(max_length=250, verbose_name='留言内容')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='留言用户')
    add_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}: {}'.format(self.user, self.content)

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name
