"""hitol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.views.static import serve

import xadmin

from .settings import MEDIA_ROOT  # STATIC_ROOT,

from account.views import ModifyView, ResetView, ForgetPwdView, ActiveUserView, RegisterView, LogoutView, LoginView, \
    IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<pk>.*)/$', ActiveUserView.as_view(), name='active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^reset/(?P<pk>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),

    url(r'^course/', include('course.urls', namespace='course')),
    url(r'^school/', include('school.urls', namespace='school')),
    url(r'^user/', include('account.urls', namespace='user')),

    url(r'^admin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)$', serve, {'document_root':STATIC_ROOT}),
]
