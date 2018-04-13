# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from account.models import UserProfile

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'院系')
    image = models.ImageField(upload_to='school/%Y/%m', verbose_name=u'照片', max_length=100)
    desc = models.TextField(verbose_name=u'介绍')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')

    class Meta:
        verbose_name = u'院系'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def get_teacher_list(self):
        return self.teacher_set.all()

    def get_student_nums(self):
        return self.student_set.all().count()

    def get_student_list(self):
        return self.student_set.all()

    def get_course_nums(self):
        return self.course_set.all().count()

    def get_course_list(self):
        return self.course_set.all()


class Teacher(models.Model):
    user = models.OneToOneField(UserProfile, verbose_name=u'用户')
    tid = models.CharField(max_length=6, verbose_name=u'教师号')
    name = models.CharField(max_length=50, verbose_name=u'姓名', default=u'')
    image = models.ImageField(default=u'teacher/default.png', upload_to='teacher/%Y/%m', verbose_name=u'照片',
                              max_length=100)
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default=u'female',
                              verbose_name=u'性别')
    age = models.IntegerField(default=18, verbose_name=u'年龄')
    school = models.ForeignKey(School, verbose_name='院系')
    start = models.DateField(verbose_name=u'参加工作时间')
    title = models.CharField(max_length=20, verbose_name=u'教师职称')
    detail = models.TextField(verbose_name=u'更多介绍')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()

    def get_course_list(self):
        return self.course_set.all()

    def get_course(self):
        return self.course_set.order_by('-fav_nums')[:1]


class Student(models.Model):
    user = models.OneToOneField(UserProfile, verbose_name=u'用户')
    sid = models.CharField(max_length=9, verbose_name=u'学号', default=u'')
    nickname = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
    image = models.ImageField(default=u'student/default.png', upload_to='student/%Y/%m', verbose_name=u'照片',
                              max_length=100)
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default=u'male',
                              verbose_name=u'性别')
    school = models.ForeignKey(School, verbose_name='院系')

    class Meta:
        verbose_name = u'学生'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.nickname

