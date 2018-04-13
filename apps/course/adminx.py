# -*- coding: utf-8 -*-

import xadmin

from .models import CourseNote, CourseResource, Lesson, Chapter, BannerCourse, Course
from school.models import School


class ChapterInline(object):
    model = Chapter
    extra = 0


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseNoteInline(object):
    model = CourseNote
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'image', 'learn_nums', 'fav_nums', 'click_nums',
                    'add_time']  # , 'get_lesson_nums', 'go_to'
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'image', 'learn_nums', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'image', 'learn_nums', 'fav_nums', 'click_nums',
                   'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['learn_nums', 'fav_nums', 'click_nums']
    list_editable = ['degree', 'desc']
    inlines = [CourseNoteInline, ChapterInline, CourseResourceInline]#LessonInline,
    # refresh_times = [3, 5]
    style_fields = {'detail': 'ueditor'}
    model_icon = 'fa fa-book'
    import_excel = False

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        obj = self.new_obj  # 课程
        obj.save()
        if obj.school is not None:
            school = obj.school  # 课程外键
            school.course_nums = Course.objects.filter(school=school).count()
            school.save()

    '''
	def post(self, request, *args, **kwargs):
		if 'excel' in request.FILES:
			pass
		return super(CourseAdmin, self).post(request, args, kwargs)
	'''


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'fav_nums', 'image', 'learn_nums', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'fav_nums', 'image', 'learn_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'fav_nums', 'image', 'learn_nums', 'click_nums',
                   'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums']
    exclude = ['click_nums']
    inlines = [ChapterInline, CourseResourceInline]#LessonInline,
    model_icon = 'fa fa-book'

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class ChapterAdmin(object):
    list_display = ['course', 'index', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']
    inlines = [LessonInline]


class LessonAdmin(object):
    list_display = ['chapter', 'index', 'name', 'add_time']
    search_fields = ['chapter', 'name']
    list_filter = ['chapter__name', 'name', 'add_time']
    model_icon = 'fa fa-video-camera'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


class CourseNoteAdmin(object):
    list_display = ['course', 'note', 'teacher', 'add_time']
    search_fields = ['course', 'note', 'teacher']
    list_filter = ['course', 'note', 'teacher', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseNote, CourseNoteAdmin)
