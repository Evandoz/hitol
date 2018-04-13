# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField

from school.models import Teacher, School


# Create your models here.

class Course(models.Model):
    school = models.ForeignKey(School, verbose_name=u'课程院系', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, verbose_name=u'教师')
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    category = models.CharField(choices=(('co', u'公选课'), ('li', u'限选课')), max_length=2, default=u'co',
                                verbose_name=u'课程类别')
    tag = models.CharField(max_length=50, default=u'', verbose_name=u'课程标签')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath='course/ueditor',
                          filePath='course/ueditor', default=u'')
    degree = models.CharField(choices=(('ju', u'初级'), ('mi', u'中级'), ('hi', u'高级')), default=u'ju', verbose_name=u'难度',
                              max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    image = models.ImageField(upload_to='course/%Y/%m', default=u'course/default.png', verbose_name=u'封面图', max_length=100)
    need_know = models.CharField(max_length=300, verbose_name=u'课程须知', default=u'')
    teacher_tell = models.CharField(max_length=300, verbose_name=u'教师告诉你', default=u'')
    learn_nums = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_chapter_nums(self):
        # 课程章节数目
        return self.chapter_set.all().count()

    def get_course_chapter(self):
        # 课程章节
        return self.chapter_set.all()

    def get_learn_students(self):
        return self.usercourse_set.all()[:12]

    def get_course_note(self):
        return self.coursenote_set.all().order_by('add_time')

    def get_new_note(self):
        return self.coursenote_set.all().order_by('-add_time')[:1]


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  # 不生成表


class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    index = models.IntegerField(default=1, verbose_name=u'章节号')
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}.{1}'.format(self.index, self.name)

    def get_chapter_lesson(self):
        # 章节
        return self.lesson_set.all()


class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name=u'章节')
    index = models.IntegerField(default=1, verbose_name=u'课时序号')
    name = models.CharField(max_length=100, verbose_name=u'课时名称')
    url = models.CharField(max_length=200, default='', verbose_name=u'视频链接')
    video = models.FileField(upload_to=u'course/video/%Y/%m', default=u'', verbose_name=u'视频文件', max_length=300)
    time = models.IntegerField(default=0, verbose_name=u'视频时长')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课时'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}.{1}'.format(self.index, self.name)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'文件名')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseNote(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    note = models.TextField(verbose_name=u'课程公告', default=u'')
    teacher = models.ForeignKey(Teacher, verbose_name=u'教师')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'发布时间')

    class Meta:
        verbose_name = u'课程公告'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}-{1}'.format(self.teacher, self.course)
