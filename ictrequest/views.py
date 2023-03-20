from django.shortcuts import render

def home(request):
	page_title = 'Home'
	context = {
		'title':page_title,
	}
	return render(request, 'ictrequest/home.html', context)
