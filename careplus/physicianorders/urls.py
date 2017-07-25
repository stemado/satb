
from django.conf.urls import url

from careplus.physicianorders import views

urlpatterns = [
    
    url(r'^create/$', views.createPhysicianOrder, name='createPhysicianOrder'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.editPhysicianOrder, name='editPhysicianOrder'),
    url(r'^(?P<id>[0-9]+)/$', views.order, name='order'),
    url(r'^$', views.orders, name='orders'),

]

from django.conf.urls import url

from careplus.physicianorders import views

urlpatterns = [
    
    url(r'^create/$', views.createPhysicianOrder, name='createPhysicianOrder'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.editPhysicianOrder, name='editPhysicianOrder'),
    url(r'^(?P<id>[0-9]+)/$', views.order, name='order'),
    url(r'^$', views.orders, name='orders'),

]

