
from django.conf.urls import url

from careplus.residents import views

urlpatterns = [
    url(r'^active_medication/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/$', views.active_medications, name='active_medications'),
    url(r'^overdue_medications/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/$', views.overdue_medications, name='overdue_medications'),
    url(r'^all_medications/(?P<id>[0-9]+)/$', views.medications, name='medications'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<id>[0-9]+)/$', views.resident, name='resident'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^emergency/$', views.emergencycontact, name='emergencycontact'),
    url(r'^$', views.residents, name='residents'),

]

