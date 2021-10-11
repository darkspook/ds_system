from django.shortcuts import render
from django.http import HttpResponse
from .models import Asset

def home(request):
	assets = Asset.objects.all()
	return render(request, 'ict_inventory/home.html', {'assets':assets})

