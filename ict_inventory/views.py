from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Asset, Component, EndUser, Type
from .forms import AssetForm, ComponentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['ict'])
def home(request):
	# assets = Asset.objects.order_by('-date_acquired')
	assets = Asset.objects.order_by('-date_last_modified')
	types = Type.objects.order_by('pk')
	years = assets.dates('date_acquired', 'year')
	yeardata, maxval = generatebarchart(request)
	# print('Year: ', years)
	context = {
			'assets':assets[:10], #top 10
			# 'assets':assets,
			'types':types,
			'data':generatepiechart(request),
			'latest':assets.latest('date_last_modified'),
			'years':years,
			'yeardata':yeardata,
			'maxval':maxval,
		}
	# print('Bar data: ', generatebarchart(request))
	# print('Context: ',context)
	return render(request, 'ict_inventory/home.html', context)

def search(request):
	if request.method == 'POST':
		#searchbox = request.POST['searchbox']
		category = request.POST['category']
		search_q = request.POST['searchq']

		if category == 'asset':
			multi_q = Q(Q(name__icontains = search_q) | Q(description__icontains = search_q) | Q(model__icontains = search_q) | Q(location__name__icontains = search_q) | Q(end_user__first_name__icontains = search_q) | Q(end_user__last_name__icontains = search_q))
			result = Asset.objects.filter(multi_q)
		else:
			multi_q = Q(Q(name__icontains = search_q) | Q(description__icontains = search_q) | Q(model__icontains = search_q))
			result = Component.objects.filter(multi_q)
		
		context = {
			'category':category,
			'searchq':search_q,
			'results':result,
		}
		# print('Result', result)
		print('Context', context)
		return render(request, 'ict_inventory/search.html', context)
	else:
		return render(request, 'ict_inventory/search.html',{})

# Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset

def asset_clone(request, pk):
	# print("Inside clone")
	asset = get_object_or_404(Asset, pk=pk)
	if request.method == 'GET':
		form = AssetForm(instance=asset)
		return render(request, 'ict_inventory/asset_clone.html', {'asset':asset, 'form':form})
	else:
		try:
			form = AssetForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.save()
			new_asset = Asset.objects.values('id').latest('pk').get('id')
			print("New clonned asset: ", new_asset)
			messages.success(request, 'Asset was added successfully.')
			return redirect('ict_inventory:asset_detail', new_asset)
		except ValueError:
			return render(request, 'ict_inventory/asset_clone.html', {'form':form, 'error':'Invalid data entered.'})

class AssetCreateView(CreateView):
	model = Asset
	template_name = 'ict_inventory/asset_new.html'
	#fields = ['name', 'description', 'property_num', 'brand', 'model', 'serial_num', 'unit_value', 'date_acquired', 'location', 'remarks', 'image', 'end_user', 'status', 'asset_type']
	form_class = AssetForm

	# def form_valid(self, form): #-- will get the current login user
	# 	form.instance.author = self.request.user
	# 	return super().form_valid(form)

class AssetUpdateView(SuccessMessageMixin, UpdateView):
	model = Asset
	template_name = 'ict_inventory/asset_update.html'
	#fields = ['name', 'description', 'property_num', 'brand', 'model', 'serial_num', 'unit_value', 'date_acquired', 'location', 'remarks', 'image', 'end_user', 'status', 'asset_type']
	form_class = AssetForm
	success_message = "Asset was updated successfully"

class AssetDeleteView(DeleteView):
	model = Asset
	success_url = reverse_lazy('ict_inventory:home')

class AssetListView(ListView):
	model = Asset
	context_object_name = "assets"
	ordering = ['-date_acquired']

class AssetDetailView(DetailView):
	model = Asset

def delete_image(request, pk):
	asset = get_object_or_404(Asset, pk=pk)
	if request.method == 'POST':
		if asset.image:
			asset.image.delete()
	return redirect('ict_inventory:asset_detail', pk=pk)


# Component - Component - Component - Component - Component - Component - Component - Component - Component
def component_clone(request, pk):
	# print("Inside clone")
	component = get_object_or_404(Component, pk=pk)
	if request.method == 'GET':
		form = ComponentForm(instance=component)
		return render(request, 'ict_inventory/component_clone.html', {'component':component, 'form':form})
	else:
		try:
			form = ComponentForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.save()
			new_component = Component.objects.values('asset_id').latest('pk').get('asset_id') #get asset_id of newly created component
			print("New clonned Component: ", new_component)
			messages.success(request, 'Component was added successfully.')
			return redirect('ict_inventory:component_listview', new_component)
		except ValueError:
			return render(request, 'ict_inventory/component_clone.html', {'form':form, 'error':'Invalid data entered.'})

def component_listview(request, pk):
	#print("PK: ", pk)
	asset = get_object_or_404(Asset, pk=pk)
	components = Component.objects.filter(asset=asset)
	return render(request, 'ict_inventory/component_listview.html', {'components':components, 'asset':asset})

class ComponentDeleteView(DeleteView):
	model = Component
	# success_url = reverse_lazy('ict_inventory:component_listview', component.asset_id)
	def get_success_url(self):
		return reverse('ict_inventory:component_listview', kwargs={'pk': self.object.asset_id})

# def component_deleteview(request, pk):
# 	component = get_object_or_404(Component, pk=pk)
# 	print('Component: ', component)
# 	if request.method == 'POST':
# 		component.delete()
# 		return redirect('ict_inventory:component_listview', component.asset_id)

def component_updateview(request, pk):
	component = get_object_or_404(Component, pk=pk)
	if request.method == 'GET':
		form = ComponentForm(instance=component)
		return render(request, 'ict_inventory/component_update.html', {'component':component, 'form':form})
	else:
		try:
			form = ComponentForm(request.POST, request.FILES, instance=component)
			form.save()
			messages.success(request, 'Component was updated successfully.')
			return redirect('ict_inventory:component_listview', component.asset_id)
		except ValueError:
			return render(request, 'ict_inventory/component_update.html', {'component':component, 'form':form, 'error':'Invalid data entered.'})

def component_delete_image(request, pk):
	component = get_object_or_404(Component, pk=pk)
	if request.method == 'POST':
		if component.image:
			component.image.delete()
	return redirect('ict_inventory:component_listview', component.asset_id)

def component_add(request, pk): # Add Component inside an Asset
	asset = get_object_or_404(Asset, pk=pk)
	form = ComponentForm(initial={'asset': asset.pk, 'brand': asset.brand})
	if request.method == 'GET':
		return render(request, 'ict_inventory/component_add.html', {'asset':asset, 'form':form, })
	else:
		try:
			form = ComponentForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.save()
			messages.success(request, 'Component was added successfully.')
			return redirect('ict_inventory:component_listview', pk)
		except ValueError:
			return render(request, 'ict_inventory/component_add.html', {'form':ComponentForm(), 'error':'Invalid data entered.'})

class ComponentCreateView(SuccessMessageMixin, CreateView): # New Component in Navigation
	model = Component
	template_name = 'ict_inventory/component_new.html'
	form_class = ComponentForm
	success_message = "Component was created successfully"

	def get_success_url(self):
		return reverse('ict_inventory:component_listview', kwargs={'pk': self.object.asset_id})

def generate_prop_num(request):
	return None

def generatepiechart(request): #Asset Distribution
	t = () #tuple
	typecount = Type.objects.count()
	# latest = Asset.objects.latest('date_last_modified')
	# latest = Asset.objects.latest('date_acquired')
	# print('Latest: ', latest)
	for i in range(1, typecount+1):
		count = Asset.objects.filter(asset_type=i).count()
		t += count,
	data = str(t)[1:-1] #remove open close parenthesis 
	# print('data: ', data)
	return data

def generatebarchart(request): #Yearly Asset Acquisition
	t = ()
	yearcount = Asset.objects.dates('date_acquired', 'year')
	# for i in range(1, assetcount+1):
	for i in yearcount:
		# print(str(i)[:-6])
		count = Asset.objects.filter(date_acquired__year=str(i)[:-6]).count()
		# print("Count: ",i,count)
		t += count,
	data = str(t)[1:-1]
	maxval = round(max(t)/10)*10
	# print("Data: ",data)
	return data, maxval+5
	# return None

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