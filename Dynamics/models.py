from django.db import models

# 关注列表
class followings(models.Model):
    uid = models.PositiveBigIntegerField(unique=True, verbose_name='UID')
    name = models.CharField(max_length=20, unique=True, verbose_name='昵称')
    name_history = models.JSONField(null=True, blank=True, default=list, verbose_name='昵称历史')
    sign = models.CharField(null=True, blank=True, max_length=100, verbose_name='个性签名')
    face = models.URLField(null=True, blank=True, verbose_name='头像')
    info = models.JSONField(null=True, blank=True, verbose_name='原始数据')
    _class = models.ForeignKey('follow_class', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='类型')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name='关注列表'
        verbose_name_plural='关注列表'

# 分类

class follow_class(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='分类名称')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name='类型列表'
        verbose_name_plural='类型列表'