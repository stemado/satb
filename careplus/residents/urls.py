
from django.conf.urls import url

from careplus.residents import views

urlpatterns = [
    url(r'^active_medication/$', views.active_medications, name='activeMedications'),
    url(r'^overdue_medications/$', views.overdue_medications, name='overdueMedications'),
    url(r'^all_medications/$', views.medications, name='medications'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<id>[0-9]+)/$', views.resident, name='resident'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^emergency/$', views.emergencycontact, name='emergencycontact'),
    url(r'^$', views.residents, name='residents'),

]

