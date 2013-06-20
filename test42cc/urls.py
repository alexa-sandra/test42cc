import os
from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from django.contrib import admin
from person import views
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^accounts/', include('accounts.urls')),
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       url(r'^$', views.index, name='index'),
                       url(r'^edit/', views.edit, name='edit'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^requests/', views.storedRequests, name='requests'),
                       url(r'^admin_tools/', include('admin_tools.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

try:
    if settings.DEBUG:# defined in manage.py when the first arg is "runserver"
        urlpatterns += patterns('',
                                (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                 {'document_root': settings.MEDIA_ROOT}),
                                (r'^media-admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.
                                join(settings.MEDIA_ROOT, settings.ADMIN_MEDIA_PREFIX)}), )
except NameError:
    pass