from django.forms import ModelForm
from .models import Delivery
from django import forms
from django.utils.timezone import datetime

def generate_iarno():
	last_record = Delivery.objects.last()
	today = datetime.now()
	print(today)
	current = "{}-{}".format(today.year, today.month) #2021-10
	if not last_record == None: #check if last record exist
		last_no = str(last_record)[-3:]
		#print("Last record exist, IAR NO: "+current + "-" + str(int(last_no) + 1).zfill(3))
		return current + "-" + str(int(last_no) + 1).zfill(3)
	else:
		#print("Last record does not exist, IAR NO: "+current+"-001")
		return current + "-001"

class DeliveryForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(DeliveryForm, self).__init__(*args, **kwargs)
		self.fields['iar_no'].initial = generate_iarno()
		self.fields['date_delivered'].initial = datetime.now()

	class Meta:
		model = Delivery
		fields = ['iar_no', 'supplier', 'purpose', 'date_delivered', 'image',]