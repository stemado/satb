from django.conf.urls import include, url
from careplus.medications import views
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetView

# app_name = 'medications'
urlpatterns = [

    url(r'^create_medication/(?P<resident_id>[0-9]+)/$', views.createMedication, name='createMedication'),
    url(r'^$', views.active_medications, name='activeMedications'),
    url(r'^all_medications/$', views.medications, name='medications'),
    url(r'^overdue_medications/$', views.overdue_medications, name='overdueMedications'),
    url(r'^test/$', views.EditMedicationUpdate.as_view(), name='testMedication'),
    url(r'^(?P<id>[0-9]+)/$', views.medication, name='medication'),
    url(r'^testcsv/$', views.csv_view, name='csvView'),
    url(r'^mar/(?P<mar_id>[0-9]+)/$', views.mar, name='mar'),
    # url(r'^testpdf/$', views.pdfNewView, name='pdfview'),
    url(r'^edit_medication/(?P<id>[0-9]+)/$', views.editMedication, name='editMedication'),
    url(r'^status/(?P<medication>[0-9]+)/(?P<rx>[0-9]+)/$', views.acceptRefuse, name='acceptRefuse'),
]
