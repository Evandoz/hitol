# -*- coding: utf-8 -*-

import xadmin

from .models import Teacher, School


class SchoolAdmin(object):
    list_display = ['name', 'image', 'desc', 'students', 'course_nums', 'click_nums']
    search_fields = ['name', 'image', 'desc', 'students', 'course_nums', 'click_nums']
    list_filter = ['name', 'image', 'desc', 'students', 'course_nums', 'click_nums']


# relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['tid', 'school', 'name', 'image', 'age', 'title', 'detail', 'points', 'click_nums', 'fav_nums']
    search_fields = ['tid', 'school', 'name', 'image', 'age', 'start', 'title', 'detail', 'points', 'click_nums', 'fav_nums']
    list_filter = ['tid', 'school', 'name', 'image', 'age', 'start', 'title', 'detail', 'points', 'click_nums', 'fav_nums']


xadmin.site.register(School, SchoolAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
