# get_all_followings
# 获取所有的关注列表。（如果用户设置保密会没有任何数据）

import os
import django
from bilibili_api import sync
from bilibili_api import user

# my_self = user.User(int(input('请输入B站的用户UID：')))
my_self = user.User(4516259)
get_all_followings = sync(my_self.get_all_followings())

if len(get_all_followings) == 0:
    print("用户设置保密或未关注任何用户。")
    exit()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyServer.settings')
django.setup()
from Dynamics.models import followings

for f in get_all_followings:
    error_list = []
    try:
        u = user.User(f)
        info = sync(u.get_user_info())
        if len(followings.objects.filter(uid=f)) == 0:
            print('> 新关注 [{}] {}'.format(f,info['name']))
            followings.objects.create(uid=f, # UID
                                  name=info['name'], # 名称
                                  sign=info['sign'], # 个性签名
                                  face=info['face'], # 头像
                                  info=info) # 元信息
        else:
            up_info = followings.objects.get(uid=f)
            if info['name'] != up_info.name:
                print('> [{}]改名为[{}]。'.format(up_info.name,info['name']))
                up_info.name_history.append(up_info.name)
                up_info.name = info['name']
            if info['sign'] != up_info.sign:
                print('> [{}]的个性签名修改为：{}\n原个性签名：{}。'.format(info['name'], info['sign'], up_info.sign))
                up_info.sign = info['sign']
            if info['face'] != up_info.face:
                print('> [{}]的头像修改为：{}。'.format(info['name'], info['face']))
                up_info.face = info['face']
            up_info.info = info
            up_info.save()
    except:
        error_list.append(f)
    for e in error_list:
        print('用户[{}]出现了错误。'.format(e))
