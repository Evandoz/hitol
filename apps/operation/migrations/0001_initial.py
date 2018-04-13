# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-05 22:13
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='\u8bc4\u8bba')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='\u8bfe\u7a0b')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u8bc4\u8bba',
                'verbose_name_plural': '\u8bfe\u7a0b\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_id', models.IntegerField(default=0, verbose_name='\u56de\u590d\u76ee\u6807')),
                ('reply_type', models.IntegerField(choices=[('1', '\u8bc4\u8bba'), ('2', '\u56de\u590d')], default=1, verbose_name='\u56de\u590d\u7c7b\u578b')),
                ('content', models.TextField(verbose_name='\u56de\u590d\u5185\u5bb9')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operation.CourseComment', verbose_name='\u56de\u590d\u8bc4\u8bba')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='\u8bfe\u7a0b')),
                ('from_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_id', to=settings.AUTH_USER_MODEL, verbose_name='\u56de\u590d\u7528\u6237')),
                ('to_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_id', to=settings.AUTH_USER_MODEL, verbose_name='\u76ee\u6807\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u56de\u590d',
                'verbose_name_plural': '\u56de\u590d',
            },
        ),
        migrations.CreateModel(
            name='UserAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u59d3\u540d')),
                ('mobile', models.CharField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('course', models.CharField(max_length=50, verbose_name='\u8bfe\u7a0b\u540d')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u54a8\u8be2',
                'verbose_name_plural': '\u7528\u6237\u54a8\u8be2',
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6536\u85cf\u65f6\u95f4')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='\u8bfe\u7a0b')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u5b66\u751f')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u8bfe\u7a0b',
                'verbose_name_plural': '\u7528\u6237\u8bfe\u7a0b',
            },
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_id', models.IntegerField(default=0, verbose_name='\u6570\u636eID')),
                ('fav_type', models.IntegerField(choices=[('1', '\u8bfe\u7a0b'), ('2', '\u673a\u6784'), ('3', '\u6559\u5e08')], default=1, verbose_name='\u6536\u85cf\u7c7b\u578b')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6536\u85cf\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6536\u85cf',
                'verbose_name_plural': '\u7528\u6237\u6536\u85cf',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=0, verbose_name='\u63a5\u6536\u7528\u6237')),
                ('message', models.CharField(max_length=500, verbose_name='\u6d88\u606f\u5185\u5bb9')),
                ('has_read', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u8bfb')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6536\u85cf\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6d88\u606f',
                'verbose_name_plural': '\u7528\u6237\u6d88\u606f',
            },
        ),
        migrations.CreateModel(
            name='UserVideoTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DecimalField(decimal_places=6, max_digits=10)),
                ('has_watch', models.BooleanField(default=False, verbose_name='\u89c2\u770b\u5b8c\u6bd5')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u8bb0\u5f55\u65f6\u95f4')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='\u8bfe\u7a0b')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Lesson', verbose_name='\u8bfe\u65f6')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u89c6\u9891\u8fdb\u5ea6',
                'verbose_name_plural': '\u89c6\u9891\u8fdb\u5ea6',
            },
        ),
    ]