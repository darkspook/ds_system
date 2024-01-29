from django.db import models
import os
from django.utils.timezone import datetime
from delivery_inspection.models import Delivery
from django.db.utils import IntegrityError
from django.urls import reverse

class CompletedDIA(models.Model):
	iar_no = models.CharField(max_length=11, unique=True)
	inspection_date = models.DateTimeField()
	delivery_date = models.DateField()
	purpose = models.TextField()
	with_ris_no = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "Completed DIA"

	def __str__(self):
		return "Delivery: "+self.purpose+" as of "+self.delivery_date

	def get_completed_dia():
		completed_dia_recent = CompletedDIA.objects.latest('inspection_date')
		# completed_dia_recent = CompletedDIA.objects.filter(with_ris_no=False)
		# print('completed_dia_recent: ',completed_dia_recent.inspection_date)
		# delivery = Delivery.objects.filter(date_inspected__isnull=False, deliverable=1, date_inspected__gte='2023-12-18 23:55:55')
		delivery = Delivery.objects.filter(date_inspected__isnull=False, deliverable=1, date_inspected__gt=str(completed_dia_recent.inspection_date))
		# print('delivery: ',delivery)

		for obj in delivery:
			completed_dia = CompletedDIA()
			completed_dia.iar_no = obj.iar_no
			completed_dia.inspection_date = obj.date_inspected
			completed_dia.delivery_date = obj.date_delivered
			completed_dia.purpose = obj.purpose
			try:
				completed_dia.save()
				# print('save completed_dia: ',completed_dia)
			except IntegrityError:
				print('***IntegrityError***')
				print('***Saving Failed: DUPLICATE DATA on get_completed_dia***')

	def get_completed_dia_init():
		today = datetime.now()
		current_year = "{}-{}-{}".format(today.year,'01','01')
		# print(current_year)

		delivery = Delivery.objects.filter(date_inspected__isnull=False, deliverable=1, date_inspected__gt=current_year)
		print("delivery: ",delivery)
		
		for obj in delivery:
			completed_dia = CompletedDIA()
			completed_dia.iar_no = obj.iar_no
			completed_dia.inspection_date = obj.date_inspected
			completed_dia.delivery_date = obj.date_delivered
			completed_dia.purpose = obj.purpose
			try:
				completed_dia.save()
				print('***Initialize Successful***')
			except IntegrityError:
				print('***IntegrityError***')
				print('***Saving Failed: DUPLICATE DATA on get_completed_dia_init***')

class IssuingRIS(models.Model):
	ris_no = models.CharField(max_length=11, unique=True) #2021-10-001
	delivery_date = models.DateField()
	purpose = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_issued = models.DateTimeField(null=True, blank=True)
	# remarks = models.TextField()

	class Meta:
		verbose_name_plural = "Issuing RIS"

	def __str__(self):
		return "RIS No. "+self.ris_no+" as of "+self.delivery_date.strftime("%b. %d, %Y")
	
	def get_absolute_url(self):
		return reverse('risgen:issuingris_detail', kwargs={'pk': self.pk})

	def assign_ris_no():
		# completed_dia = CompletedDIA.objects.all()
		completed_dia = CompletedDIA.objects.filter(with_ris_no=False)

		# print('completed_dia: ',completed_dia)
		for obj in completed_dia:
			issuing_ris = IssuingRIS()
			issuing_ris.ris_no = IssuingRIS.generate_ris_no()
			issuing_ris.delivery_date = obj.delivery_date
			issuing_ris.purpose = obj.purpose
			# print('issuing_ris: ', issuing_ris)
			# IssuingRIS.flag_completed_dia(issuing_ris.delivery_date, issuing_ris.purpose)
			# issuing_ris.save()
			try:
				issuing_ris.save()
				# print('assign_ris_no SAVE')
				# print('issuing_ris: ', issuing_ris)
			except IntegrityError:
				print('***IntegrityError***')
				print('***Saving Failed: ASSIGN RIS NO***')
			# This will update CompletedDIA's with_ris_no = True
			try:
				completed_dia2 = CompletedDIA.objects.get(delivery_date=issuing_ris.delivery_date, purpose=issuing_ris.purpose)
				completed_dia2.with_ris_no = True
				completed_dia2.save()
			except IntegrityError:
				print('***IntegrityError***')
				print('***Saving Failed: assign_ris_no: WITH RIS NO***')


	def generate_ris_no():
		last_record = IssuingRIS.objects.last()
		# print('Last record: ',last_record.ris_no)
		today = datetime.now()
		# print(today)
		current = "{}-{}".format(today.year, today.strftime('%m')) #2021-10
		# print(current)
		if not last_record == None: #check if last record exist
			last_no = str(last_record.ris_no)[-3:]
			return current + "-" + str(int(last_no) + 1).zfill(3)
		else:
			#print("Last record does exist, IAR NO: "+current+"-001")
			return current + "-001"

class IssuingRISItems(models.Model):
	ris_no = models.ForeignKey(IssuingRIS, on_delete=models.CASCADE)
	stock_no = models.IntegerField(null=True)
	unit = models.CharField(max_length=100)
	item_description = models.TextField()
	qty = models.CharField(max_length=7)
	remarks = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Issuing RIS Items"

	def __str__(self):
		return str(self.ris_no)+", Stock No. "+str(self.stock_no)