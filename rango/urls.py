#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:49429
# datetime:2019/4/24 16:02
# software: PyCharm
from django.conf.urls import include, url
from . import views

urlpatterns = [
               url(r'^$', views.index, name='index'),
               url(r'^about/$', views.about, name='about'),
               url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
               url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
               #url(r'^category/(?P<category_name_url>[\w\-]+)/$', views.category, name='category'),
               url(r'^add_category/$', views.add_category, name='add_category'),
               url(r'register/$', views.register, name='register'),
               url(r'login/$',views.user_login,name='login'),
               url(r'^logout/$', views.user_logout, name='logout'),
               ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)