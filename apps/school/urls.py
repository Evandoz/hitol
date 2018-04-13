from django.conf.urls import url

from school.views import TeacherDetailView, TeacherListView, UserFavView, SchoolTeacherView, SchoolDescView, SchoolCourseView, SchoolHomeView, UserAskView, SchoolView

urlpatterns = [
	url(r'^list/$', SchoolView.as_view(), name='school_list'),
	url(r'^ask/$', UserAskView.as_view(), name='user_ask'),
	url(r'^home/(?P<school_id>\d+)/$', SchoolHomeView.as_view(), name='school_home'),
	url(r'^course/(?P<school_id>\d+)/$', SchoolCourseView.as_view(), name='school_course'),
	url(r'^desc/(?P<school_id>\d+)/$', SchoolDescView.as_view(), name='school_desc'),
	url(r'^school_teacher/(?P<school_id>\d+)/$', SchoolTeacherView.as_view(), name='school_teacher'),
	url(r'^fav/$', UserFavView.as_view(), name='user_fav'),

	url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
	url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]