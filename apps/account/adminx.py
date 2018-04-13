# -*- coding: utf-8 -*-

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from django.contrib.auth.models import User

from .models import Banner, EmailVerifyRecord, UserProfile


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "工大在线后台管理"
    site_footer = "工大在线"
    menu_style = "accordion"

'''
class TeacherAdmin(UserAdmin):
    list_display = ['tid', 'nickname', 'gender', 'age', 'school', 'title', 'image']
    search_fields = ['tid', 'nickname', 'gender', 'age', 'school', 'title', 'image']
    list_filter = ['tid', 'nickname', 'gender', 'age', 'school', 'title', 'image']


class StudentAdmin(UserAdmin):
    list_display = ['sid', 'nickname', 'gender', 'school', 'image']
    search_fields = ['sid', 'nickname', 'gender', 'school', 'image']
    list_filter = ['sid', 'nickname', 'gender', 'school', 'image']
'''

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-user'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    model_icon = 'fa fa-picture-o'


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
#xadmin.site.register(Teacher, TeacherAdmin)
#xadmin.site.register(Student, StudentAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
