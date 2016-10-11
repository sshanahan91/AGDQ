from django.conf.urls import url
from . import views

urlpatterns = [

    #event/{event_id}
    url(r'(/){1}(?P<event_id>[a-z]{1,10}[0-9]{0,4})[/]?$', views.detail, name='event_detail_id'),

    #event/{event_p_id}
    url(r'(/){1}(?P<event_id>[0-9]+)[/]?$', views.detail_id, name='event_detail'),

	#/tracker (index)
    url(r's[/]?', views.index, name='index'),

]