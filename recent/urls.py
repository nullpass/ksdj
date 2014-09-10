# recent/urls.py
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    #
    url(r'^$',                    views.Index.as_view(),            name='index'),
    #url(r'^(?P<pk>\d+)/update/$', views.ClientUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/$',        views.RecentDetailView.as_view(), name='detail'),
    #url(r'^add/$',                views.ClientCreateView.as_view(), name='create'),
)
