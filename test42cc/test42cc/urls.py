from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from django.contrib import admin
from person import views
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^admin_tools/', include('admin_tools.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
