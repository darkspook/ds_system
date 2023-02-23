from django.db import models

# Create your models here.
from django.db import models
from datetime import date
from django.urls import reverse

class Type(models.Model):
	name = models.CharField(max_length=50, unique=True)
	symbol = models.CharField(max_length=10, blank=True)
	remarks = models.CharField(max_length=200, blank=True)
	date_last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('ictinv:assettype_list')

class Location(models.Model):
	name = models.CharField(max_length=50, unique=True)
	remarks = models.CharField(max_length=200, blank=True)
	date_last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('ictinv:location_list')

class Brand(models.Model):
	name = models.CharField(max_length=50, unique=True)
	remarks = models.CharField(max_length=200, blank=True)
	date_last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('ictinv:brand_list')

class EndUser(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	remarks = models.CharField(max_length=200, blank=True)
	date_last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.last_name+", "+self.first_name

	def get_absolute_url(self):
		return reverse('ictinv:enduser_list')

class Asset(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	property_num = models.CharField(max_length=50, blank=True)
	brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
	model = models.CharField(max_length=50, blank=True)
	serial_num = models.CharField(max_length=50, blank=True)
	unit_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date_acquired = models.DateField(default=date.today)
	location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
	SERV = "serviceable"
	UNSERV = "unserviceable"
	NLN = "no longer needed"
	STATUS_CHOICES = [(SERV, 'serviceable'),(UNSERV, 'unserviceable'),(NLN, 'no longer needed')]
	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=SERV)
	image = models.ImageField(upload_to='asset/images/', blank=True)
	remarks = models.CharField(max_length=200, blank=True)
	date_last_modified = models.DateTimeField(auto_now=True)
	end_user = models.ForeignKey(EndUser, null=True, on_delete=models.SET_NULL)
	asset_type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		#print('pk= '+str(self.pk))
		#print('reverse = '+str(reverse('asset_detail', kwargs={'pk': str(self.pk)})))
		return reverse('ictinv:asset_detail', kwargs={'pk': self.pk})

class Component(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	property_num = models.CharField(max_length=50, blank=True)
	brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
	model = models.CharField(max_length=50, blank=True)
	serial_num = models.CharField(max_length=50, blank=True)
	unit_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date_acquired = models.DateField(default=date.today)
	status = models.CharField(max_length=50, choices=Asset.STATUS_CHOICES, default=Asset.SERV)
	image = models.ImageField(upload_to='component/images/', blank=True)
	remarks = models.CharField(max_length=200, blank=True)
	date_last_modified = models.DateTimeField(auto_now=True)
	asset = models.ForeignKey(Asset, null=True, on_delete=models.SET_NULL)
	location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
	end_user = models.ForeignKey(EndUser, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('ictinv:component_listview', kwargs={'pk': self.pk})