from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Asset, Component, EndUser
from .forms import AssetForm, ComponentForm

def asset_detail(request, pk):
	print("inside asset_detail")
	asset = get_object_or_404(Asset, pk=pk)
	if request.method == 'GET':
		return render(request, 'ict_inventory/asset_detail.html', {'asset':asset})

def asset_list(request, pk):
	asset = Asset.objects.filter(pk=pk)
	return render(request, 'ict_inventory/home.html', {'asset':asset})

def component_new(request):
	if request.method == 'GET':
		return render(request, 'ict_inventory/component_new.html', {'form':ComponentForm()})
	else:
		try:
			form = ComponentForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.created_by = request.user #set created_by to the logged in user
			new.save()
			return redirect('ict_inventory:home')
		except ValueError:
			return render(request, 'ict_inventory/component_new.html', {'form':ComponentForm(), 'error':'Invalid data entered'})

def asset_new(request):
	if request.method == 'GET':
		return render(request, 'ict_inventory/asset_new.html', {'form':AssetForm()})
	else:
		try:
			form = AssetForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.save()
			return redirect('ict_inventory:home')
		except ValueError:
			return render(request, 'ict_inventory/asset_new.html', {'form':AssetForm(), 'error':'Invalid data entered'})

def generate_prop_num(request):
	return None

def home(request):
	assets = Asset.objects.all()
	return render(request, 'ict_inventory/home.html', {'assets':assets})

def getAssets(request):
	assets = Asset.objects.filter(end_user_id=1)
	#get all component id with asset_id = the above asset_id
	return None

def test(request):
	enduser = EndUser.objects.filter(id=1)
	print(enduser)
	assets = Asset.objects.filter(end_user_id=1)
	print(assets.count())
	components = Component.objects.filter(asset_id=1)
	print(components)
	return render(request, 'ict_inventory/test.html', {'assets':assets, 'components':components, 'enduser':enduser})