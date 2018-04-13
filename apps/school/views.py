# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Teacher, School
from course.models import Course
from operation.models import UserFavorite

from .forms import UserAskForm


# Create your views here.

class SchoolView(View):
    def get(self, request):
        all_schools = School.objects.all()

        for school in all_schools:
            school.students = school.get_student_nums()
            school.course_nums = school.get_course_nums()
            school.save()

        search_keywords = request.GET.get('keywords', u'')
        if search_keywords:
            all_schools = all_schools.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        hot_schools = all_schools.order_by('-click_nums')[:3]

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_schools = all_schools.order_by('-students')
            elif sort == 'courses':
                all_schools = all_schools.order_by('-course_nums')

        school_nums = all_schools.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_schools, 5, request=request)
        schools = p.page(page)

        return render(request, 'school-list.html', {
            'all_schools': schools,
            'school_nums': school_nums,
            'hot_schools': hot_schools,
            'sort': sort
        })


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class SchoolHomeView(View):
    def get(self, request, school_id):

        current_page = 'home'

        school = School.objects.get(id=int(school_id))

        school.click_nums += 1
        school.save()

        all_courses = school.course_set.all()
        all_teachers = school.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=school.id, fav_type=2):
                has_fav = True
        return render(request, 'school-detail-homepage.html', {
            'current_page': current_page,
            'school': school,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'has_fav': has_fav
        })


class SchoolCourseView(View):
    def get(self, request, school_id):

        current_page = 'course'

        school = School.objects.get(id=int(school_id))
        all_courses = school.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=school.id, fav_type=2):
                has_fav = True
        return render(request, 'school-detail-course.html', {
            'current_page': current_page,
            'all_courses': all_courses,
            'school': school,
            'has_fav': has_fav
        })


class SchoolDescView(View):
    def get(self, request, school_id):

        current_page = 'desc'

        school = School.objects.get(id=int(school_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=school.id, fav_type=2):
                has_fav = True
        return render(request, 'school-detail-desc.html', {
            'current_page': current_page,
            'school': school,
            'has_fav': has_fav
        })


class SchoolTeacherView(View):
    def get(self, request, school_id):

        current_page = 'teacher'

        school = School.objects.get(id=int(school_id))
        all_teachers = school.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=school.id, fav_type=2):
                has_fav = True
        return render(request, 'school-detail-teacher.html', {
            'current_page': current_page,
            'all_teachers': all_teachers,
            'school': school,
            'has_fav': has_fav
        })


class UserFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户是否登录、
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 记录已存在，表示取消收藏
            exist_records.delete()

            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                school = School.objects.get(id=int(fav_id))
                school.fav_nums -= 1
                if school.fav_nums < 0:
                    school.fav_nums = 0
                school.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0 and request.user.is_student:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    school = School.objects.get(id=int(fav_id))
                    school.fav_nums += 1
                    school.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        search_keywords = request.GET.get('keywords', u'')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(title__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        hot_teachers = all_teachers.order_by('-click_nums')[:5]

        teacher_nums = all_teachers.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        teachers = p.page(page)

        return render(request, 'teacher-list.html', {
            'all_teachers': teachers,
            'sort': sort,
            'teacher_nums': teacher_nums,
            'hot_teachers': hot_teachers
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher.click_nums += 1
        teacher.save()

        teacher_courses = Course.objects.filter(teacher=teacher)

        has_teacher_fav = False
        has_school_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teacher_fav = True

            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.school.id, fav_type=2):
                has_school_fav = True

        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:2]

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'teacher_courses': teacher_courses,
            'hot_teachers': hot_teachers,
            'has_teacher_fav': has_teacher_fav,
            'has_school_fav': has_school_fav
        })
