from django.shortcuts import render
from django.http import HttpResponse
from .models import Event

# Create your views here.
def index(request):
	context = {

	}
	return render(request, 'events/index.html', context)

def detail(request, event_id):
	event = Event.objects.get(event_id__startswith=event_id)
	context = {
		"event": event,
	}
	return render(request, 'events/details.html', context)


def detail_id(request, event_id):
	event = Event.objects.get(id=event_id)	
	context = {
		'event': event,
	}
	return render(request, 'events/details.html', context)
