from django.shortcuts import render
from django.http import HttpResponse
#from .models import Event

# Create your views here.
def index(request):
	context = {

	}
	return render(request, 'events/index.html', context)

def detail(request, event_id):
	return HttpResponse(event_id)