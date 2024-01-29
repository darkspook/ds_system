from django.forms import ModelForm
from .models import Delivery, PartialDelivery
from django import forms
from django.utils.timezone import datetime
from django.contrib.auth.forms import  AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, Textarea, DateInput, FileInput, Select

DELIVERABLE_CHOICES = ( 
    ("1", "Goods"), 
    ("2", "Services")
) 

def generate_iarno():
	last_record = Delivery.objects.last()
	today = datetime.now()
	print(today)
	current = "{}-{}".format(today.year, today.strftime('%m')) #2021-10
	print(current)
	if not last_record == None: #check if last record exist
		last_no = str(last_record)[-3:]
		#print("Last record exist, IAR NO: "+current + "-" + str(int(last_no) + 1).zfill(3))
		return current + "-" + str(int(last_no) + 1).zfill(3)
	else:
		#print("Last record does not exist, IAR NO: "+current+"-001")
		return current + "-001"

class PartialDeliveryForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PartialDeliveryForm, self).__init__(*args, **kwargs)
		self.fields['date_delivered'].initial = datetime.now()

	#delivery = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'IAR Number',"disabled":"disabled"}))
	remarks = forms.CharField(widget=Textarea(attrs={'class': 'form-control','placeholder': 'Remarks'}))
	date_delivered = forms.CharField(widget=DateInput(attrs={'class': 'form-control','placeholder': 'Date of Delivery'}))
	
	class Meta:
		model = PartialDelivery
		fields = ['date_delivered', 'remarks']
			

class DeliveryForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(DeliveryForm, self).__init__(*args, **kwargs)
		self.fields['iar_no'].initial = generate_iarno()
		self.fields['date_delivered'].initial = datetime.now()

	iar_no = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'IAR Number'}))
	supplier = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Supplier'}))
	purpose = forms.CharField(widget=Textarea(attrs={'class': 'form-control','placeholder': 'Purpose'}))
	date_delivered = forms.CharField(widget=DateInput(attrs={'class': 'form-control','placeholder': 'Date of Delivery'}))
	image = forms.ImageField(widget=FileInput(attrs={'class': 'form-control'}), required=False)
	inspector = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Inspector'}), required=False)
	deliverable = forms.ChoiceField(widget=Select(attrs={'class': 'form-control'}), choices=DELIVERABLE_CHOICES)

	class Meta:
		model = Delivery
		fields = ['iar_no', 'deliverable', 'supplier', 'purpose', 'date_delivered', 'inspector', 'image',]

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))