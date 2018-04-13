# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from account.models import UserProfile
from course.models import Lesson, Chapter, Course


# Create your models here.

class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机号')
    course = models.CharField(max_length=50, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    comment = models.TextField(verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return unicode(user)

    def get_comment_reply(self):
        return self.replycomment_set.all()


class ReplyComment(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    comment_id = models.ForeignKey(CourseComment, verbose_name=u'回复评论')
    reply_id = models.IntegerField(default=0, verbose_name=u'回复目标')
    reply_type = models.IntegerField(choices=(('1', u'评论'), ('2', u'回复')), default=1, verbose_name=u'回复类型')
    content = models.TextField(verbose_name=u'回复内容')
    from_id = models.ForeignKey(UserProfile, verbose_name=u'回复用户', related_name='from_id')
    to_id = models.ForeignKey(UserProfile, verbose_name=u'目标用户', related_name='to_id')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'回复'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return unicode(comment_id)


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    fav_id = models.IntegerField(default=0, verbose_name=u'数据ID')
    fav_type = models.IntegerField(choices=(('1', u'课程'), ('2', u'机构'), ('3', u'教师')), default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'收藏时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return unicode(self.user)


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接收用户')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'收藏时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return unicode(self.user)


class UserCourse(models.Model):
    student = models.ForeignKey(UserProfile, verbose_name=u'学生')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'收藏时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}-{1}'.format(self.user, self.course)


class UserVideoTime(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    lesson = models.ForeignKey(Lesson, verbose_name=u'课时')
    time = models.DecimalField(max_digits=10, decimal_places=6)
    has_watch = models.BooleanField(default=False, verbose_name=u'观看完毕')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'记录时间')

    class Meta:
        verbose_name = u'视频进度'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}:{1}-{2}'.format(self.user, self.course, self.lesson)
