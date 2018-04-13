from django.conf.urls import url

from account.views import AddLessonView, AddResourceView, AddNoteView, AddChapterView, CourseInfoEditView, CourseEditView, CommentCountView, UserDataView, UserMessageView, UserFavCourseView, UserFavTeacherView, UserFavSchoolView, UserCourseView, \
    UserEmailView, UserEmailCodeView, UserPwdView, UserImageView, UserInfoView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', UserImageView.as_view(), name='user_image'),
    url(r'^pwd/update/$', UserPwdView.as_view(), name='user_pwd'),
    url(r'^email/code/$', UserEmailCodeView.as_view(), name='user_email_code'),
    url(r'^email/update/$', UserEmailView.as_view(), name='user_email'),
    url(r'^course/$', UserCourseView.as_view(), name='user_course'),
    url(r'^fav/school/$', UserFavSchoolView.as_view(), name='user_fav_school'),
    url(r'^fav/teacher/$', UserFavTeacherView.as_view(), name='user_fav_teacher'),
    url(r'^fav/course/$', UserFavCourseView.as_view(), name='user_fav_course'),
    url(r'^course/edit/(?P<course_id>\d+)/$', CourseEditView.as_view(), name='course_edit'),
    url(r'^course/edit/info/(?P<course_id>\d+)/$', CourseInfoEditView.as_view(), name='course_edit_info'),
    url(r'^course/edit/chapter/(?P<course_id>\d+)/$', AddChapterView.as_view(), name='course_edit_chapter'),
    url(r'^course/edit/lesson/(?P<chapter_id>\d+)/$', AddLessonView.as_view(), name='course_edit_lesson'),
    url(r'^course/edit/resource/(?P<course_id>\d+)/$', AddResourceView.as_view(), name='course_edit_resource'),
    url(r'^course/edit/note/$', AddNoteView.as_view(), name='course_edit_note'),
    url(r'^data/$', UserDataView.as_view(), name='user_data'),
    url(r'^data/(?P<course_id>\d+)/$', CommentCountView.as_view(), name='comment_count'),
    url(r'^message/$', UserMessageView.as_view(), name='user_message'),
]
