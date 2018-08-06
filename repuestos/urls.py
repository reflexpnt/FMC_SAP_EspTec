from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.part_list),
    #url(r'^$', include('django.contrib.auth.urls')),
    #url(r'^$', views.part_pdf),
    url(r'^pdf/(?P<pdf_art_id>[0-9]+)/$', views.part_pdf, name='part_pdf'),
    url(r'^(?P<pk>[0-9]+)/$', views.part_detail, name='part_detail'),
    url(r'^accounts/', include('django.contrib.auth.urls')),


]