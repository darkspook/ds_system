from django.forms import ModelForm
from .models import IssuingRISItems, IssuingRIS
from django import forms
from django.utils.timezone import datetime
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, Textarea, DateInput, FileInput, Select

class IssuingRISForm(ModelForm):
	"""docstring for IssuingRISForm"""
	def __init__(self, *args, **kwargs):
		super(IssuingRISForm, self).__init__(*args, **kwargs)
		self.fields['ris_no'].initial = IssuingRIS.generate_ris_no()
		self.fields['delivery_date'].initial = datetime.now()

	ris_no = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
	delivery_date = forms.CharField(widget=DateInput(attrs={'class': 'form-control','placeholder': 'Date of Delivery'}))
	purpose = forms.CharField(widget=Textarea(attrs={'class': 'form-control','placeholder': 'Purpose', 'style':'height:50px;'}))

	class Meta:
		model = IssuingRIS
		fields = ['ris_no', 'delivery_date', 'purpose',]

class IssuingRISItemsForm(ModelForm):
	"""docstring for IssuingRISItemsForm"""
	def __init__(self, *args, **kwargs):
		super(IssuingRISItemsForm, self).__init__(*args, **kwargs)

	stock_no = forms.IntegerField(widget=TextInput(attrs={'class': 'form-control'}))
	unit = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
	item_description = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'style':'height:50px;'}), required=False)
	qty = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
	remarks = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'style':'height:50px;'}), required=False)

	class Meta:
		model = IssuingRISItems
		fields = ['stock_no','unit','item_description','qty','remarks']
		