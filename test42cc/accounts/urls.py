from django.conf.urls import patterns, url
from test42cc.person import views



urlpatterns = patterns('',
     url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
     url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
     url(r'^profile',  views.index, name='index'),
     )
