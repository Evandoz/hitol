# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField
from school.models import Student, Teacher
from course.models import CourseResource, Lesson, Chapter, Course


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetForm(forms.Form):
    password = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)


class UploadSImageForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['image']


class UploadTImageForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['image']


class UploadSInfoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['sid', 'nickname', 'gender', 'school']


class UploadTInfoForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['tid', 'name', 'gender', 'school', 'title', 'start']


class UploadCourseInfoForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['desc', 'tag', 'degree', 'need_know', 'teacher_tell']


class UploadChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['index', 'name']


class UploadLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['index', 'name', 'url', 'video']
