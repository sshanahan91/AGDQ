from django.conf.urls import url
from . import views

urlpatterns = [

    #run/{run_id}
    url(r'(/){1}(?P<run_id>[0-9]+)', views.detail, name='run_detail'),

	#runs (index)
    url(r's[/]?$', views.index, name='index'),

]