from datetime import datetime

from django.db import models

from django.utils import timezone


class OrgProfile(models.Model):
    """
        机构信息
    """
    name = models.CharField(max_length=150, unique=True, null=False, blank=False, verbose_name='机构名称')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name='机构上级')
    code = models.IntegerField(default=0, null=False, blank=False, verbose_name='编码')
    org_type_choices = (
        (1, '科室'),
        (2, '班组'),
        (3, '对组'),
    )
    org_type = models.PositiveSmallIntegerField(choices=org_type_choices, null=False, blank=False, verbose_name='机构类型')
    category_type_choices = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
    )
    category_type = models.IntegerField(choices=category_type_choices, null=False, blank=False, verbose_name='层级')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '机构信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}, {}'.format(self.name, self.get_category_type_display())

    @classmethod
    def new_orgs_month(cls):
        return cls.objects.filter(add_time__month=datetime.now().month)
