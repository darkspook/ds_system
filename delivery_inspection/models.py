from django.db import models
from django.contrib.auth.models import User

class Delivery(models.Model):
	iar_no = models.CharField(max_length=11, unique=True) #2021-10-001
	supplier = models.CharField(max_length=100)
	purpose = models.TextField()
	date_delivered = models.DateField()
	image = models.ImageField(upload_to='delivery_inspection/images/%Y/%m', blank=True)
	inspected_by = models.CharField(max_length=100, blank=True) #get curren login inspector
	date_inspected = models.DateTimeField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	inspector = models.CharField(max_length=100, blank=True) #this will be a sort of reminder who is the actual inspector that will press accept & inspect

	class Meta:
		verbose_name_plural = "deliveries"

	def __str__(self):
		#return self.iar_no + " Purpose: " +self.purpose
		return self.iar_no

class PartialDelivery(models.Model):
	delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
	remarks = models.CharField(max_length=200, blank=True)
	date_delivered = models.DateField()
	inspected_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	class Meta:
		verbose_name_plural = "partial deliveries"
	def __str__(self):
		return "Partial delivery for " +str(self.delivery)