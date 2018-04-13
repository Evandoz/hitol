from django.conf.urls import url

from course.views import VideoTimeView, CourseVideoView, AddReplyView, AddCommentView, CourseCommentView, CourseInfoView, CourseDetailView, \
    CourseListView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^add_reply/$', AddReplyView.as_view(), name='add_reply'),
    url(r'^video/(?P<video_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    url(r'^video/time/$', VideoTimeView.as_view(), name='video_time'),
]
