from django.conf.urls import url
from . import views

urlpatterns = [

    #donor/{donor_id}
    url(r'/(?P<donor_id>[0-9]+)$', views.detail, name='donor_detail'),

	#donors (index)
    url(r's', views.index, name='index'),

]