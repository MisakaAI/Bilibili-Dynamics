from django.db import models

# 关注列表
class followings(models.Model):
    uid = models.PositiveBigIntegerField(unique=True, verbose_name='UID')
    name = models.CharField(max_length=20, unique=True, verbose_name='昵称')
    name_history = models.JSONField(null=True, blank=True, default=list, verbose_name='昵称历史')
    note = models.CharField(null=True, blank=True, max_length=100, verbose_name='简介') 
    sign = models.CharField(null=True, blank=True, max_length=100, verbose_name='个性签名')
    info = models.JSONField(null=True, blank=True, verbose_name='原始数据')
    show = models.BooleanField(default=False, verbose_name='默认展示启用')
    _class = models.ForeignKey('follow_class', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='类型')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name='关注列表'
        verbose_name_plural='关注列表'

# 分类
class follow_class(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='分类名称')
    show = models.BooleanField(default=True, verbose_name='导航栏中展示')
    star = models.BooleanField(default=True, verbose_name='默认列表启用')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name='类型列表'
        verbose_name_plural='类型列表'

# 屏蔽词语
class block_words(models.Model):
    key = models.CharField(max_length=30, unique=True, verbose_name='关键词')

    def __str__(self) -> str:
        return self.key

    class Meta:
        verbose_name='屏蔽词语'
        verbose_name_plural='屏蔽词语'