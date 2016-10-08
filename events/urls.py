from django.conf.urls import url
from . import views

urlpatterns = [
	#/tracker (index)
    url(r'index', views.index, name='index'),

    #event/{event_id}
    url(r'event/(?P<event_id>[0-9]+)$', views.detail, name='event_detail'),

]