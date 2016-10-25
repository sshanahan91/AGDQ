from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile

# Create your views here.
def index(request):
	all_donors = Profile.objects.all()
	paginator = Paginator(all_donors, 50)
	page = request.GET.get('page')

	# https://docs.djangoproject.com/en/1.9/topics/pagination/
	try:
		donors = paginator.page(page)
	except PageNotAnInteger:
		donors = paginator.page(1)
		page = 1
	except EmptyPage:
		donors = paginator.page(paginator.num_pages)
	
	page_range = []
	for num in range(int(page)-5, int(page)+6):
		if (num > 0) and (num <= paginator.num_pages):
			page_range.append(str(num))
	context = {
		'donors'      : donors,
		'pages'       : paginator,
		'page_range'  : page_range,
		'current_page': page,
	}
	return render(request, 'profiles/profile_index.html', context)

def detail(request, donor_id):
	donor = Profile.objects.get(user_id=donor_id)
	context = {
		"donor": donor,
	}
	return render(request, 'profiles/profile_details.html', context)