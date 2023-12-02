from django.shortcuts import render
from django.http import JsonResponse
from bilibili_api import user, sync
import time
from .models import *

def index(request):
    _class = follow_class.objects.all()
    followings_list = {}
    for f in _class:
        followings_list[f.name] = {}
        for u in followings.objects.filter(_class=f):
            followings_list[f.name][u.name] = {
                 "uid": u.uid,
                 "note": u.note,
            }
    followings_list['None'] = {}
    for u in followings.objects.filter(_class=None):
            followings_list['None'][u.uid] = u.name
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
    def get_beijing_time(timestamp):
        utc_time = time.gmtime(timestamp)
        beijing_timestamp = time.mktime(utc_time) + 8 * 3600
        beijing_time = time.gmtime(beijing_timestamp)
        return time.strftime('%Y-%m-%d %H:%M', beijing_time)
    if class_id:
        _class = follow_class.objects.filter(id=class_id)
        dynamics_list = {}
        for f in _class:
            dynamics_list[f.name] = {}
            for f_user in followings.objects.filter(_class=f):
                u = user.User(f_user.uid)
                p = sync(u.get_dynamics())
                u_dynamics = {
                    "uid": f_user.uid,
                    "note": f_user.note,
                    "dynamics": []
                }
                print(p)
                if 'cards' in p:
                    # 如果有动态
                    for i in p['cards']:
                        if i['desc']['type'] == 8:
                            timestamp = i['card']['pubdate']
                            if is_within_seven_days(timestamp) and '【直播回放】' not in i['card']['title']:
                                # u_dynamics['face']=
                                u_dynamics['dynamics'].append({
                                    "aid": i['card']['aid'],
                                    "link": i['card']['short_link_v2'],
                                    "pic": i['card']['pic'],
                                    "title": i['card']['title'],
                                    "tname": i['card']['tname'],
                                    "pubdate": get_beijing_time(timestamp),
                                })
                if len(u_dynamics['dynamics']) != 0:
                    dynamics_list[f.name][f_user.name] = u_dynamics
    else:
        dynamics_list = {}
    all_class = follow_class.objects.all()
    context = {
        'class_id': class_id,
        'class': all_class,
        'data': dynamics_list
    }
    # return JsonResponse(dynamics_list,json_dumps_params={'ensure_ascii':False})
    return render(request, 'Dynamics/dynamics.html', context)
