import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from orgs.models import OrgProfile
from users.models import UserProfile, Message


class UserInfo(View):
    def get(self, request):
        # 人数统计
        all_orgs = OrgProfile.objects.all()[:10]
        org_users_count = [{
            '组织': org.name,
            '人数': org.userprofile_set.all().count()
        } for org in all_orgs]

        # 最近用户
        recent_users = UserProfile.objects.order_by('-date_joined')[:10]
        recent_users = [{
            'username': user.username,
            'email': user.email,
        } for user in recent_users]

        # 用户总数
        all_users_count = UserProfile.objects.count()

        # 今日新用户
        new_user_count_today = UserProfile.new_users_today().count()

        # 组织总数
        all_orgs_count = OrgProfile.objects.count()

        # 本月新加入组织
        all_orgs_count_month = OrgProfile.new_orgs_month().count()

        # 用户留言
        user_message = Message.objects.all().order_by('-id')[:7]
        user_message = [{
            'name': msg.user.username,
            'content': msg.content,
            'time': '{}月{}日'.format(msg.add_time.month, msg.add_time.day)
        } for msg in user_message]

        json_result = json.dumps({
            'org_users_count': org_users_count,
            'recent_users': recent_users,
            'all_users_count': all_users_count,
            'new_user_count_today': new_user_count_today,
            'all_orgs_count': all_orgs_count,
            'all_orgs_count_month': all_orgs_count_month,
            'user_message': user_message,
        }, ensure_ascii=False)

        return HttpResponse(json_result, content_type='application/json')


def format_add_time(add_time):
    return '{}-{}-{}'.format(
        add_time.year,
        add_time.month,
        add_time.day
    )


class OrgInfo(View):
    def get(self, request):
        all_orgs_list = OrgProfile.objects.all()
        org_info_list = [{
            'name': org.name,
            'code': org.code,
            'org_type': org.get_org_type_display(),
            'category_type': org.get_category_type_display(),
            'add_time': format_add_time(org.add_time)
        } for org in all_orgs_list]

        json_result = json.dumps({
            'orgs': org_info_list
        }, ensure_ascii=False)

        return HttpResponse(json_result, content_type='application/json')


class UpdateUserPassword(View):
    def post(self, request):
        password = request.POST.get('password', None)
        if password is not None:
            pass

        return HttpResponse('{status: "successed"}', content_type='application/json')


class GoodsList(View):
    def get(self, request):
        data_path = r'C:\Users\Administrator\Desktop\z1b8jp\mock\goods.json'
        with open(data_path, encoding='utf8', mode='r') as f:
            json_data = f.read()

        return HttpResponse(json_data, content_type='application/json')
