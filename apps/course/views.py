# -*- coding: utf-8 -*-
import decimal

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseResource, Lesson, Chapter, Course
from account.models import UserProfile
from school.models import Student, School
from operation.models import UserVideoTime, UserMessage, ReplyComment, UserCourse, CourseComment, UserFavorite

from utils.mixin_utils import LoginRequireMixin


# Create your views here.

class CourseListView(View):
    # 课程列表
    def get(self, request):
        all_schools = School.objects.all()
        all_courses = Course.objects.all()

        hot_courses = all_courses.order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords', u'')
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords) | Q(tag__icontains=search_keywords) | Q(
                    school__name__icontains=search_keywords) | Q(teacher__name__icontains=search_keywords))

        category = request.GET.get('ct', '')
        if category:
            all_courses = all_courses.filter(category=category)

        school_id = request.GET.get('sc', '')
        if school_id:
            all_courses = all_courses.filter(school_id=int(school_id))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'new':
                all_courses = all_courses.order_by('-add_time')
            elif sort == 'students':
                all_courses = all_courses.order_by('-learn_nums')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'all_schools': all_schools,
            'category': category,
            'school_id': school_id,
            'sort': sort
        })


class CourseDetailView(View):
    # 课程详情
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_school = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.school.id, fav_type=2):
                has_fav_school = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag).exclude(id=int(course_id))[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_school': has_fav_school
        })


class CourseInfoView(LoginRequireMixin, View):
    # 课程章节
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 用户是否关联课程
        if request.user.is_student:
            user_courses = UserCourse.objects.filter(student=request.user, course=course)
            if user_courses:
                user_time = UserVideoTime.objects.filter(user=request.user, course=course)
            else:
                user_time = []
                user_courses = UserCourse(student=request.user, course=course)
                course.learn_nums += 1
                course.save()
                user_courses.save()
        else:
            user_time = []

        user_courses = UserCourse.objects.filter(course=course)  # 获取当前课程所有记录

        all_users = [user_course.student.id for user_course in user_courses]  # 筛选课程用户ID
        all_user_courses = UserCourse.objects.filter(student_id__in=all_users)  # 通过ID获取用户课程

        all_courses = [user_course.course.id for user_course in all_user_courses]  # 筛选课程ID
        courses = Course.objects.filter(id__in=all_courses).order_by('-click_nums')[:5]  # 通过ID获取课程

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'user_time': user_time,
            'courses': courses,
            'all_resources': all_resources
        })


class CourseCommentView(LoginRequireMixin, View):
    # 课程评论
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        user_courses = UserCourse.objects.filter(course=course)  # 获取当前课程所有记录

        all_users = [user_course.student.id for user_course in user_courses]  # 筛选课程用户ID
        all_user_courses = UserCourse.objects.filter(student_id__in=all_users)  # 通过ID获取用户课程

        all_courses = [user_course.course.id for user_course in all_user_courses]  # 筛选课程ID
        courses = Course.objects.filter(id__in=all_courses).order_by('-click_nums')[:3]  # 通过ID获取课程

        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComment.objects.filter(course=course).order_by('-add_time')
        return render(request, 'course-comment.html', {
            'course': course,
            'courses': courses,
            'all_resources': all_resources,
            'all_comments': all_comments
        })


class AddCommentView(View):
    # 添加评论
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户是否登录、
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comment', u'')
        if course_id > 0 and comment:
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comment = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


class AddReplyView(View):
    # 添加评论
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户是否登录、
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        course = Course.objects.get(id=int(course_id))
        comment_id = request.POST.get('comment_id', 0)
        reply_id = request.POST.get('reply_id', 0)
        reply_type = request.POST.get('reply_type', 0)
        content = request.POST.get('content', u'')
        to_id = request.POST.get('to_id', 0)
        to_user = UserProfile.objects.get(id=int(to_id))
        if comment_id > 0 and content:
            reply_comment = ReplyComment()
            comment_id = CourseComment.objects.get(id=int(comment_id))
            reply_comment.course = course
            reply_comment.comment_id = comment_id
            reply_comment.reply_id = int(reply_id)
            reply_comment.reply_type = int(reply_type)
            reply_comment.content = content
            reply_comment.from_id = request.user
            reply_comment.to_id = to_user
            reply_comment.save()

            if request.user != to_user:
                user_message = UserMessage()
                user_message.user = to_user.id
                user_message.message = u'您有新的回复：' + content
                user_message.has_read = False
                user_message.save()

            return HttpResponse('{"status":"success", "msg":"回复成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"回复失败"}', content_type='application/json')


class CourseVideoView(View):
    # 课程视频
    def get(self, request, video_id):
        lesson = Lesson.objects.get(id=int(video_id))
        course = lesson.chapter.course

        # 用户是否关联课程
        if request.user.is_student:
            user_courses = UserCourse.objects.filter(student=request.user, course=course)
            if not user_courses:
                user_courses = UserCourse(student=request.user, course=course)
                course.learn_nums += 1
                course.save()
                user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)  # 获取当前课程所有记录

        all_users = [user_course.student.id for user_course in user_courses]  # 筛选课程用户ID
        all_user_courses = UserCourse.objects.filter(student_id__in=all_users)  # 通过ID获取用户课程

        all_courses = [user_course.course.id for user_course in all_user_courses]  # 筛选课程ID
        courses = Course.objects.filter(id__in=all_courses).order_by('-click_nums')[:5]  # 通过ID获取课程

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'courses': courses,
            'lesson': lesson,
            'all_resources': all_resources
        })


class VideoTimeView(LoginRequireMixin, View):
    def post(self, request):

        course_id = request.POST.get('course_id', 0)
        lesson_id = request.POST.get('lesson_id', 0)
        time = request.POST.get('time', 0.000000)

        course = Course.objects.get(id=int(course_id))
        lesson = Lesson.objects.filter(chapter__course=course).get(id=int(lesson_id))

        exist_record = UserVideoTime.objects.filter(user=request.user, course=course, lesson=lesson)
        if exist_record:
            exist_record.update(time=decimal.Decimal(time))
        else:
            user_video_time = UserVideoTime()
            user_video_time.user = request.user
            user_video_time.course = course
            user_video_time.lesson = lesson
            user_video_time.time = decimal.Decimal(time)
            user_video_time.has_watch = False
            user_video_time.save()

        return HttpResponse('{"status":"success", "msg":"记录成功"}', content_type='application/json')
