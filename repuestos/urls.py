from django.conf.urls import  include, url
#from django.conf.urls.defaults import *
from . import views
from repuestos.views import postsJson

urlpatterns = [
    #->>url(r'^$', views.part_list, name='index'),


    url(r'^ajax_posts$', views.postsJson , name='ajax_posts'),
    #url(r'^$', views.part_list, name='index'),

    url(r'^$', views.show, name='index'),


    #url(r'^$', include('django.contrib.auth.urls')),
    #url(r'^$', views.part_pdf),
    url(r'^pdf/(?P<pdf_art_id>[0-9]+)/$', views.part_pdf, name='part_pdf'),
    url(r'^(?P<pk>[0-9]+)/$', views.part_detail, name='part_detail'),

    url(r'^sapnum/(?P<numeroParte>[a-zA-Z0-9_]+)/$', views.ara_detail, name='ara_detail'),

    url(r'^accounts/', include('django.contrib.auth.urls')),
#    url(r'^art/new/$', views.articulo_new, name='articulo_new'),
    url(r'^art/(?P<pk>[0-9]+)/edit/$', views.articulo_edit, name='articulo_edit'),


    url(r'^datatables', views.show, name='datatables'),


]



#urlpatterns += url(regex=r'^$', view='postsJson', name='ajax_posts'),
