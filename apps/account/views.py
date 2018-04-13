# -*- coding: utf-8 -*-
import json
from django.shortcuts import render_to_response, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.db.models import Count

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Banner, EmailVerifyRecord, UserProfile
from operation.models import UserMessage, UserFavorite, CourseComment, ReplyComment, UserCourse
from school.models import Student, Teacher, School
from course.models import CourseNote, CourseResource, Lesson, Chapter, Course
from .forms import UploadLessonForm, UploadChapterForm, UploadCourseInfoForm, UploadSInfoForm, UploadTInfoForm, UploadSImageForm, UploadTImageForm, ResetForm, ForgetForm, RegisterForm, LoginForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequireMixin


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        # 去除轮播图
        all_banners = Banner.objects.all().order_by('index')
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        schools = School.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'banner_courses': banner_courses,
            'courses': courses,
            'schools': schools
        })


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            pass_word = login_form.cleaned_data['password']
            # user_name = request.POST.get('username', '')
            # pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            tmp = UserProfile.objects.filter(username=user_name)
            print(tmp)
            if not tmp:
                return HttpResponse('{"status":"fail","msg":"用户不存在"}', content_type='application/json')
            elif user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('{"status":"success","url":"/","msg":"登录成功，正在跳转！"}',
                                        content_type='application/json')
                    # return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('{"status":"fail","msg":"用户未激活"}', content_type='application/json')
                    # return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return HttpResponse('{"status":"fail","msg":"密码错误"}', content_type='application/json')
                # return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            # return render(request, 'login.html', {'login_form': login_form})
            return HttpResponse(json.dumps(login_form.errors), content_type='application/json')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data['email']
            pass_word = register_form.cleaned_data['password']
            # user_name = request.POST.get('email', '')
            # pass_word = request.POST.get('password', '')
            if UserProfile.objects.filter(email=user_name):
                # return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
                return HttpResponse('{"status":"fail", "msg":"用户已存在"}', content_type='application/json')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            student = Student()
            student.user = user_profile
            school = School.objects.get(id=1)
            student.school = school
            student.save()


            # 系统发送消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = u'欢迎注册'
            user_message.save()

            #send_register_email(user_name, 'register')
            # return render(request, 'login.html')
            return HttpResponse('{"status":"success", "url":"/login/"}', content_type='application/json')
        else:
            # return render(request, 'register.html', {'register_form': register_form})
            return HttpResponse(json.dumps(register_form.errors), content_type='application/json')


class ActiveUserView(View):
    def get(self, request, pk):
        all_records = EmailVerifyRecord.objects.filter(code=pk)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, pk):
        all_records = EmailVerifyRecord.objects.filter(code=pk)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'resetpwd.html', {'email': email})
        return render(request, 'login.html')


class ModifyView(View):
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd != pwd2:
                return render(request, 'resetpwd.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'resetpwd.html', {'email': email, 'reset_form': reset_form})


class UserInfoView(LoginRequireMixin, View):
    def get(self, request):

        current_page = 'info'

        all_schools = School.objects.all()

        return render(request, 'usercenter-info.html', {
            'current_page': current_page,
            'all_schools': all_schools
        })

    def post(self, request):
        if request.user.is_student:
            userinfo_form = UploadSInfoForm(request.POST, instance=request.user.student)
        elif request.user.is_teacher:
            userinfo_form = UploadTInfoForm(request.POST, instance=request.user.teacher)

        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(userinfo_form.errors), content_type='application/json')


class UserImageView(LoginRequireMixin, View):
    def post(self, request):
        if request.user.is_student:
            image_form = UploadSImageForm(request.POST, request.FILES, instance=request.user.student)
        elif request.user.is_teacher:
            image_form = UploadTImageForm(request.POST, request.FILES, instance=request.user.teacher)

        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UserPwdView(LoginRequireMixin, View):
    # 个人中心修改密码
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            if pwd != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class UserEmailCodeView(LoginRequireMixin, View):
    # 发送邮箱验证码
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已注册"}', content_type='application/json')

        send_register_email(email, 'update')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UserEmailView(LoginRequireMixin, View):
    # 修改个人邮箱
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        exist_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
        if exist_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class UserCourseView(LoginRequireMixin, View):
    def get(self, request):
        current_page = 'course'

        if request.user.is_teacher:
            user_courses = request.user.teacher.get_course_list()
        elif request.user.is_student:
            user_courses = UserCourse.objects.filter(student=request.user)

        return render(request, 'usercenter-course.html', {
            'current_page': current_page,
            'user_courses': user_courses
        })


class UserFavSchoolView(LoginRequireMixin, View):
    def get(self, request):
        current_page = 'fav'

        school_list = []
        fav_schools = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_school in fav_schools:
            school_id = fav_school.fav_id
            school = School.objects.get(id=school_id)
            school_list.append(school)
        return render(request, 'usercenter-fav-org.html', {
            'current_page': current_page,
            'school_list': school_list
        })


class UserFavTeacherView(LoginRequireMixin, View):
    def get(self, request):
        current_page = 'fav'

        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'current_page': current_page,
            'teacher_list': teacher_list
        })


class UserFavCourseView(LoginRequireMixin, View):
    def get(self, request):
        current_page = 'fav'

        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'current_page': current_page,
            'course_list': course_list
        })


class UserDataView(LoginRequireMixin, View):
    def get(self, request):
        current_page = 'data'

        if request.user.is_teacher:
            user_courses = request.user.teacher.get_course_list()

        return render(request, 'usercenter-data.html', {
            'current_page': current_page,
            'user_courses': user_courses
        })


class CommentCountView(LoginRequireMixin, View):
    def get(self, request, course_id):

        current_page = 'data'

        course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(course=course)
        students = [user_course.student for user_course in user_courses]
        comment_counts = CourseComment.objects.filter(course=course).values('user').annotate(Count('comment'))
        reply_counts = ReplyComment.objects.filter(course=course).values('from_id').annotate(Count('content'))

        join_nums = []
        for student in students:
            if student.is_student:
                tmp = {'sid': student.student.sid, 'name': student.student.nickname, 'school': student.student.school}
                for comment_coun in comment_counts:
                    if comment_coun['user'] == student.id:
                        tmp['nums'] = comment_coun['comment__count']
                        break
                    else:
                        tmp['nums'] = 0
                        continue

                for reply_count in reply_counts:
                    if student.id == reply_count['from_id']:
                        tmp['nums'] += reply_count['content__count']
                        break

                join_nums.append(tmp)

        return render(request, 'usercenter-comment.html', {
            'current_page': current_page,
            'course': course,
            'join_nums': join_nums
        })


class CourseEditView(LoginRequireMixin, View):
    # 课程章节
    def get(self, request, course_id):

        current_page = 'course'

        course = Course.objects.get(id=int(course_id))

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'usercenter-editcourse.html', {
            'current_page': current_page,
            'course': course,
            'all_resources': all_resources
        })


class CourseInfoEditView(LoginRequireMixin, View):
    # 课程章节
    def post(self, request, course_id):

        course = Course.objects.get(id=int(course_id))

        courseinfo_form = UploadCourseInfoForm(request.POST, instance=course)

        if courseinfo_form.is_valid():
            courseinfo_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(courseinfo_form.errors), content_type='application/json')


class AddChapterView(LoginRequireMixin, View):
    def post(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        chapter_form = UploadChapterForm(request.POST)

        if chapter_form.is_valid():
            index = chapter_form.cleaned_data['index']
            name = chapter_form.cleaned_data['name']
            chapter = Chapter(course=course, index=index, name=name)
            chapter.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(chapter_form.errors), content_type='application/json')


class AddLessonView(LoginRequireMixin, View):
    def post(self, request, chapter_id):
        chapter = Chapter.objects.get(id=int(chapter_id))

        #index = request.POST.get('index', 0)
        #name = request.POST.get('name', u'')
        #url = request.POST.get('url', u'')
        #video = request.FILES.get('video')

        uploadlesson_form = UploadLessonForm(request.POST, request.FILES)

        if uploadlesson_form.is_valid():
            index = uploadlesson_form.cleaned_data['index']
            name = uploadlesson_form.cleaned_data['name']
            url = uploadlesson_form.cleaned_data['url']
            video = uploadlesson_form.cleaned_data['video']
            lesson = Lesson(chapter=chapter, index=index, name=name, url=url, video=video, time=3)

            lesson.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(uploadlesson_form.errors), content_type='application/json')


class AddResourceView(LoginRequireMixin, View):
    def post(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        resourcefiles = request.FILES.getlist('resourcefile')
        for resourcefile in resourcefiles:
            resource = CourseResource(course=course, name=resourcefile.name, download=resourcefile)
            resource.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class AddNoteView(LoginRequireMixin, View):
    def post(self, request):

        course_id = request.POST.get('course_id', 0)
        content = request.POST.get('content', u'')

        course = Course.objects.get(id=int(course_id))

        if request.user.is_teacher:
            new_note = CourseNote(course=course, note=content, teacher=request.user.teacher)
            new_note.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}, {"msg":"没有权限"}', content_type='application/json')


class UserMessageView(LoginRequireMixin, View):
    def get(self, request):

        current_page = 'message'

        all_messages = UserMessage.objects.filter(user=request.user.id)

        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 3, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'current_page': current_page,
            'all_messages': messages
        })


def page_denied(request):
    # 全局403
    response = render_to_response('403.html')
    response.status_code = 403
    return response


def page_not_found(request):
    # 全局404
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def page_error(request):
    # 全局500
    response = render_to_response('500.html')
    response.status_code = 500
    return response
