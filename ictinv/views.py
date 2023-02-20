from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Asset, Component, EndUser, Type
from .forms import AssetForm, ComponentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.utils.decorators import method_decorator

#@login_required
@allowed_users(allowed_roles=['ict'])
def home(request):
	"""The Home Dashboard that will display widgets such as charts and and top 10 last modified ict.
	The data and parameters for charts are generated here via generatebarchart() function then wrap in a context.
	"""
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
	return render(request, 'ictinv/home.html', context)

@allowed_users(allowed_roles=['ict'])
def search(request):
	"""Search for keywords on both Assets and Components
	The search is case insensitive.
	The search for asset will be on name, description, model, location, enduser fistname and lastname.
	The search for component will be on name, description, model.
	"""
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
		return render(request, 'ictinv/search.html', context)
	else:
		return render(request, 'ictinv/search.html',{})

# Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset - Asset
@allowed_users(allowed_roles=['ict'])
def asset_clone(request, pk):
	"""Clone existing Asset
	Clone existing Asset details to save time and avoid retyping common information.
	The clone will only be save if you press the Save button.
	This will not clone the Asset component.
	"""
	# print("Inside clone")
	asset = get_object_or_404(Asset, pk=pk)
	if request.method == 'GET':
		form = AssetForm(instance=asset)
		return render(request, 'ictinv/asset_clone.html', {'asset':asset, 'form':form})
	else:
		try:
			form = AssetForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.save()
			new_asset = Asset.objects.values('id').latest('pk').get('id')
			print("New clonned asset: ", new_asset)
			messages.success(request, 'Asset was added successfully.')
			return redirect('ictinv:asset_detail', new_asset)
		except ValueError:
			messages.error(request, 'Invalid data entered.')
			return render(request, 'ictinv/asset_clone.html', {'form':form})

class AssetCreateView(SuccessMessageMixin,CreateView):
	"""Generic creating view for Asset
	This is New Asset in navigation"""
	model = Asset
	template_name = 'ictinv/asset_new.html'
	form_class = AssetForm
	success_message = "Asset was created successfully"

	# def get_success_url(self):
	# 	return reverse('ictinv:asset_list')

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	# def form_valid(self, form): #-- will get the current login user
	# 	form.instance.author = self.request.user
	# 	return super().form_valid(form)

class AssetUpdateView(SuccessMessageMixin, UpdateView):
	"""Generic updating view for Asset"""
	model = Asset
	template_name = 'ictinv/asset_update.html'
	form_class = AssetForm
	success_message = "Asset was updated successfully"

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class AssetDeleteView(DeleteView):
	"""Generic deleting view for Asset"""
	model = Asset
	success_url = reverse_lazy('ictinv:home')

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class AssetListView(ListView):
	"""Generic listing view for Asset"""
	model = Asset
	context_object_name = "assets"
	ordering = ['-date_acquired']

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class AssetDetailView(DetailView):
	"""Generic detail view for Asset"""
	model = Asset

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@allowed_users(allowed_roles=['ict'])
def delete_image(request, pk):
	"""Delete attached image in an Asset"""
	asset = get_object_or_404(Asset, pk=pk)
	if request.method == 'POST':
		if asset.image:
			asset.image.delete()
	return redirect('ictinv:asset_detail', pk=pk)


# Component - Component - Component - Component - Component - Component - Component - Component - Component
class ComponentAvailableListView(ListView):
	"""Generic listing view for Component Available"""
	model = Component
	context_object_name = "components"
	queryset = Component.objects.filter(end_user=None)
	template_name = 'ictinv/component_available_list.html'

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@allowed_users(allowed_roles=['ict'])
def component_clone(request, pk):
	"""Clone existing Component
	Clone existing Component details to save time and avoid retyping common information.
	The clone will only be save if you press the Save button.
	"""
	component = get_object_or_404(Component, pk=pk)
	if request.method == 'GET':
		form = ComponentForm(instance=component)
		return render(request, 'ictinv/component_clone.html', {'component':component, 'form':form})
	else:
		try:
			form = ComponentForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.save()
			new_component = Component.objects.values('asset_id').latest('pk').get('asset_id') #get asset_id of newly created component
			new_component2 = Component.objects.values('id').latest('pk').get('id') #get id of newly create component
			# print("New clonned Component: ", new_component2)
			messages.success(request, 'Component was added successfully.')
			#return redirect('ictinv:component_listview', new_component2)
			if "clone2" in request.get_full_path():
				return redirect('ictinv:component_detail', new_component2)
			else:
				return redirect('ictinv:component_listview', new_component)
		except ValueError:
			messages.error(request, 'Invalid data entered.')
			return render(request, 'ictinv/component_clone.html', {'form':form})

@allowed_users(allowed_roles=['ict'])
def component_listview(request, pk):
	"""List View function for Component"""
	#print("PK: ", pk)
	asset = get_object_or_404(Asset, pk=pk)
	components = Component.objects.filter(asset=asset)
	return render(request, 'ictinv/component_listview.html', {'components':components, 'asset':asset})

class ComponentListView(ListView):
	"""Generic listing view for Component"""
	model = Component
	context_object_name = "components"
	ordering = ['-id']

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class ComponentDetailView(DetailView):
	"""Generic detail view for Component"""
	model = Component

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class ComponentDeleteView(DeleteView):
	"""Generic deleting view for Component"""
	model = Component
	# success_url = reverse_lazy('ictinv:component_listview', component.asset_id)
	def get_success_url(self):
		#print(self.object.id)
		if self.object.asset_id == None:
			return reverse('ictinv:component_list')
		else:
			return reverse('ictinv:component_listview', kwargs={'pk': self.object.asset_id})

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@allowed_users(allowed_roles=['ict'])
def component_updateview(request, pk):
	"""Update View function for Component back to Component List View"""

	component = get_object_or_404(Component, pk=pk)
	if request.method == 'GET':
		form = ComponentForm(instance=component)
		return render(request, 'ictinv/component_update.html', {'component':component, 'form':form})
	else:
		try:
			form = ComponentForm(request.POST, request.FILES, instance=component)
			form.save()
			messages.success(request, 'Component was updated successfully.')
			if "update2" in request.get_full_path():
				return redirect('ictinv:component_detail', pk)
			else:
				return redirect('ictinv:component_listview', component.asset_id)
		except ValueError:
			messages.error(request, 'Invalid data entered.')
			return render(request, 'ictinv/component_update.html', {'component':component, 'form':form})

@allowed_users(allowed_roles=['ict'])
def component_delete_image(request, pk):
	"""Delete attached image in a Component"""
	component = get_object_or_404(Component, pk=pk)
	if request.method == 'POST':
		if component.image:
			component.image.delete()
	return redirect('ictinv:component_listview', component.asset_id)

@allowed_users(allowed_roles=['ict'])
def component_add(request, pk):
	"""Add Component inside an Asset"""
	asset = get_object_or_404(Asset, pk=pk)
	form = ComponentForm(initial={'asset':asset.pk, 'brand':asset.brand, 'property_num':asset.property_num, 'unit_value':asset.unit_value, 'date_acquired':asset.date_acquired, 'end_user':asset.end_user, 'location':asset.location})
	if request.method == 'GET':
		return render(request, 'ictinv/component_add.html', {'asset':asset, 'form':form, })
	else:
		try:
			form = ComponentForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.save()
			messages.success(request, 'Component was added successfully.')
			return redirect('ictinv:component_listview', pk)
		except ValueError:
			messages.error(request, 'Invalid data entered.')
			return render(request, 'ictinv/component_add.html', {'form':ComponentForm()})

class ComponentCreateView(SuccessMessageMixin, CreateView):
	"""Generic creating view for Component
	This is New Component in navigation"""
	model = Component
	template_name = 'ictinv/component_new.html'
	form_class = ComponentForm
	success_message = "Component was created successfully"

	def get_success_url(self):
		return reverse('ictinv:component_list')

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

# SETUP - SETUP - SETUP - SETUP - SETUP - SETUP - SETUP - SETUP - SETUP - SETUP - SETUP - SETUP
class AssetTypeCreateView(SuccessMessageMixin, CreateView):
	"""Generic creating view for Asset Type"""
	model = Type
	template_name = 'ictinv/assettype_new.html'
	success_message = "Asset Type was created successfully"
	fields = ['name', 'symbol', 'remarks']
	def get_success_url(self):
		return reverse('ictinv:assettype_list')

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class AssetTypeListView(ListView):
	"""Generic listing view for Asset Type"""
	model = Type
	template_name = 'ictinv/assettype_list.html'
	context_object_name = "assettypes"
	ordering = ['name']

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class AssetTypeUpdateView(SuccessMessageMixin, UpdateView):
	"""Generic updating view for Asset Type"""
	model = Type
	template_name = 'ictinv/assettype_update.html'
	fields = ['name', 'symbol', 'remarks']
	success_message = "Asset Type was updated successfully"

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class AssetTypeDeleteView(DeleteView):
	"""Generic deleting view for Asset Type"""
	model = Type
	template_name = 'ictinv/assettype_confirm_delete.html'
	success_url = reverse_lazy('ictinv:assettype_list')

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class EndUserCreateView(SuccessMessageMixin, CreateView):
	"""Generic creating view for End User"""
	model = EndUser
	template_name = 'ictinv/enduser_new.html'
	success_message = "End User was created successfully"
	fields = ['last_name', 'first_name', 'remarks']
	def get_success_url(self):
		return reverse('ictinv:enduser_list')

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class EndUserListView(ListView):
	"""Generic listing view for End User"""
	model = EndUser
	context_object_name = "endusers"
	ordering = ['last_name']

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class EndUserUpdateView(SuccessMessageMixin, UpdateView):
	"""Generic updating view for End User"""
	model = EndUser
	template_name = 'ictinv/enduser_update.html'
	fields = ['last_name', 'first_name', 'remarks']
	#form_class = AssetForm
	success_message = "End User was updated successfully"

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class EndUserDeleteView(DeleteView):
	"""Generic deleting view for End User"""
	model = EndUser
	success_url = reverse_lazy('ictinv:enduser_list')

	# Proper way of adding decorator to a class based view
	@method_decorator(allowed_users(allowed_roles=['ict']))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

def generate_prop_num(request):
	return None

def generatepiechart(request):
	"""Asset Distribution piechart
	Get the total count of all asset per asset type and make it as piechart data.
	"""
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

def generatebarchart(request):
	"""Yearly Asset Acquisition
	Get the total count of all asset per year acuired and make it as barchart data.
	"""
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
	"""Test function"""
	assets = Asset.objects.filter(end_user_id=1)
	#get all component id with asset_id = the above asset_id
	return None

def test(request):
	"""Test function"""
	enduser = EndUser.objects.filter(id=1)
	print(enduser)
	assets = Asset.objects.filter(end_user_id=1)
	print(assets.count())
	components = Component.objects.filter(asset_id=1)
	print(components)
	return render(request, 'ictinv/test.html', {'assets':assets, 'components':components, 'enduser':enduser})