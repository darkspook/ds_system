from django.forms import ModelForm
from .models import Asset, Component, EndUser, Brand, Location, Type
from django import forms
from django.utils.timezone import datetime
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, Textarea, DateInput, FileInput, Select

class ComponentForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ComponentForm, self).__init__(*args, **kwargs)
		self.fields['date_acquired'].initial = datetime.now()

	name = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
	description = forms.CharField(widget=Textarea(attrs={'class':'form-control', 'style':'height:50px;'}), required=False)
	property_num = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
	brand = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}), queryset=Brand.objects.all().order_by('name'))
	model = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
	serial_num = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
	unit_value = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
	date_acquired = forms.CharField(widget=DateInput(attrs={'class': 'form-control'}))
	remarks = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'style':'height:50px;'}), required=False)
	image = forms.ImageField(widget=FileInput(attrs={'class': 'form-control'}), required=False)
	asset = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}), required=False, queryset=Asset.objects.order_by('id').reverse()) #reverse so that last added asset will be on top
	status = forms.ChoiceField(widget=Select(attrs={'class': 'form-control'}), choices=Asset.STATUS_CHOICES)
	location = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}), queryset=Location.objects.all().order_by('name'))
	end_user = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}), required=False, queryset=EndUser.objects.all().order_by('last_name'))

	class Meta:
		model = Component
		fields = ['name', 'asset', 'property_num', 'brand', 'model', 'serial_num', 'unit_value', 'date_acquired', 'end_user', 'location' ,'description', 'remarks', 'image', 'status']

class AssetForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(AssetForm, self).__init__(*args, **kwargs)
		self.fields['date_acquired'].initial = datetime.now()

	name = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
	description = forms.CharField(widget=Textarea(attrs={'class':'form-control', 'style':'height:50px;'}), required=False)
	property_num = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
	brand = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}), queryset=Brand.objects.all().order_by('name'))
	model = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
	serial_num = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}), required=False)
	unit_value = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
	date_acquired = forms.CharField(widget=DateInput(attrs={'class': 'form-control'}))
	location = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}), queryset=Location.objects.all().order_by('name'))
	remarks = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'style':'height:50px;'}), required=False)
	image = forms.ImageField(widget=FileInput(attrs={'class': 'form-control'}), required=False)
	end_user = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}), queryset=EndUser.objects.all().order_by('last_name'), required=False)
	status = forms.ChoiceField(widget=Select(attrs={'class': 'form-control'}), choices=Asset.STATUS_CHOICES)
	asset_type = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}), queryset=Type.objects.all().order_by('name'))

	class Meta:
		model = Asset
		fields = ['name', 'asset_type', 'end_user', 'property_num', 'brand', 'model', 'serial_num', 'unit_value', 'date_acquired', 'location', 'description', 'remarks', 'image', 'status']