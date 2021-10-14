from django.shortcuts import render

def home(request):
	return render(request, 'portfolio/home.html')

def projects(request):
	return render(request, 'portfolio/projects.html')