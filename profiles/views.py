from django.shortcuts import render
from django.http import HttpResponse
# from .models import Profile

# Create your views here.
def index(request):
	context = {

	}
	return render(request, 'profiles/profile_index.html', context)

def detail(request, donor_id):
#	donor = donor.objects.get(donor_id__startswith=donor_id)
	context = {
#		"donor": donor,
	}
	return render(request, 'profiles/profile_details.html', context)