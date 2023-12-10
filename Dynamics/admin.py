from django.contrib import admin
from .models import *

# 管理页面顶部的文字
admin.site.site_header = '哔哩哔哩动态 Plus'
#  <title> （字符串）末尾放置的文字。
admin.site.site_title = '哔哩哔哩 (゜-゜)つロ 干杯~'
# 管理索引页顶部的文字（一个字符串）
admin.site.index_title = '管理后台'

@admin.register(followings)
class followingsAdmin(admin.ModelAdmin):
    list_display = ['name','uid','_class','note','sign','show']
    list_editable = ['_class','note','show']
    search_fields = ['name','uid']
    list_filter = ['_class']

@admin.register(follow_class)
class follow_classAdmin(admin.ModelAdmin):
    list_display = ['name','show','star']

from .models import block_words
admin.site.register(block_words)
