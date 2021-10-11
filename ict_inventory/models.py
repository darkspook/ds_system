from django.db import models

class Asset(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	unit_measure = models.CharField(max_length=50) #dropdown
	qty_prop_card = models.IntegerField(default=0)
	qty_phy_count = models.IntegerField(default=0)
	date_acquired = models.DateTimeField()
	end_user = models.CharField(max_length=50)
	location = models.CharField(max_length=100)
	remarks = models.CharField(max_length=50) #Serviceable/Unserviceable
	image = models.ImageField(upload_to='asset/images/')

	def __str__(self):
		return self.name

class Component(models.Model):
	name = models.CharField(max_length=100) # should be drop-down
	brand = models.CharField(max_length=100)
	date_acquired = models.DateTimeField()
	serial_no = models.CharField(max_length=100)
	image = models.ImageField(upload_to='component/images/')

	def __str__(self):
		return self.name