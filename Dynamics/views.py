from django.shortcuts import render
from django.http import JsonResponse
from bilibili_api import user, sync
import time
from .models import *

def index(request):
    # 获取全部分类
    _class = follow_class.objects.all()
    # 关注列表
    followings_list = {}
    # 按分类填充关注列表
    for f in _class:
        followings_list[f.name] = {
            'id': f.id,
            'data': {}
        }
        for u in followings.objects.filter(_class=f):
            followings_list[f.name]['data'][u.name] = {
                 "uid": u.uid,
                 "note": u.note,
            }
    # 添加未分类的关注
    followings_list['未分类'] = {
            'id': 1,
            'data': {}
    }
    for u in followings.objects.filter(_class=None):
            followings_list['未分类']['data'][u.uid] = u.name
    # 返回值构成
    context = {
        'data': followings_list
    }
    # return JsonResponse(followings_list,json_dumps_params={'ensure_ascii':False})
    return render(request, 'Dynamics/index.html', context)

def dynamics(request,class_id=False):

    # 判断时间是否在7天以内
    def is_within_seven_days(timestamp):
        # 获取当前时间戳
        current_timestamp = int(time.time())
        # 计算时间差
        time_difference = abs(current_timestamp - timestamp)
        # 判断时间差是否在7天以内
        seven_days_in_seconds = 7 * 24 * 60 * 60
        return time_difference <= seven_days_in_seconds

    # 将时间戳增加8小时
    def get_beijing_time(timestamp):
        # 8h * 6min * 6s * 100
        beijing_timestamp = timestamp + 8 * 3600
        # 时间戳转换为时间
        beijing_time = time.gmtime(beijing_timestamp)
        return time.strftime('%Y-%m-%d %H:%M', beijing_time)
    # 关键词屏蔽
    def block_keywords(t):
        block_list = ['直播回放','直播录像']
        for i in block_list:
            if i in t:
                return False
        return True
    # 默认展示列表
    if class_id == 0:
        _class = follow_class.objects.filter(star=True)
    # 非默认展示列表
    elif class_id == 1:
        _class = follow_class.objects.filter(star=False)
    # 按分类展示
    else:
        _class = follow_class.objects.filter(id=class_id)

    dynamics_list = {} # 动态列表
    dynamics_none = [] # 没有动态的UP列表
    for f in _class:
        dynamics_list[f.name] = {}
        if class_id == 0:
            followings_list = followings.objects.filter(_class=f, show=True)
        else:
            followings_list = followings.objects.filter(_class=f)
        for f_user in followings_list:
            u = user.User(f_user.uid)
            p = sync(u.get_dynamics())
            u_dynamics = {
                "uid": f_user.uid, # UID
                "note": f_user.note, # 备注
                "dynamics": [] # 近期动态列表
            }
            if 'cards' in p:
                u_dynamics['face'] = p['cards'][0]['desc']['user_profile']['info']['face']
                # 如果有动态
                for i in p['cards']:
                    if i['desc']['type'] == 8:
                        timestamp = i['card']['pubdate']
                        if is_within_seven_days(timestamp) and block_keywords(i['card']['title']):
                            u_dynamics['dynamics'].append({
                                "aid": i['card']['aid'],
                                "link": i['card']['short_link_v2'],
                                "pic": i['card']['pic'],
                                "title": i['card']['title'],
                                "tname": i['card']['tname'],
                                "pubdate": get_beijing_time(timestamp),
                            })
            # 如果近期动态列表数量不为0 加入 动态列表
            if len(u_dynamics['dynamics']) != 0:
                dynamics_list[f.name][f_user.name] = u_dynamics
            # 否则加入 没有动态的UP列表
            else:
                dynamics_none.append([f_user.uid,f_user.name])
    # 导航栏展示类型列表
    all_class = follow_class.objects.filter(show=True)
    # 返回值构成
    context = {
        'class_id': class_id,
        'class': all_class,
        'data': dynamics_list,
        'dynamics_none': dynamics_none
    }
    # return JsonResponse(dynamics_list,json_dumps_params={'ensure_ascii':False})
    return render(request, 'Dynamics/dynamics.html', context)
