from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import DeliveryForm, LoginForm
from .models import Delivery
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import datetime
import datetime


#def home(request):
#	return render(request, 'delivery_inspection/home.html')

def generate_report(request):
	if request.GET['reportType'] == 'dateRange':
		dateFrom = request.GET['dateFrom']
		dateTo = request.GET['dateTo'] 
		if not dateFrom or not dateTo:
			return render(request, 'delivery_inspection/reports_base.html', {'title':'No parameter provided in the'})
		else:
			dateFromf = datetime.datetime.strptime(dateFrom, '%Y-%m-%d').strftime("%b. %d, %Y")
			print(dateFromf)
			dateTof = datetime.datetime.strptime(dateTo, '%Y-%m-%d').strftime("%b. %d, %Y")
			print(dateTof)
			title = "Inspected deliveries from {} to {}".format(dateFromf, dateTof)
			# delivery = Delivery.objects.filter(date_inspected__isnull=False).order_by('date_inspected')
			delivery = Delivery.objects.filter(date_inspected__isnull=False).exclude(date_delivered__gte=dateTo).filter(date_delivered__gte=dateFrom).order_by('date_inspected')
			return render(request, 'delivery_inspection/reports_base.html', {'reports':delivery, 'title':title})
	elif(request.GET['reportType'] == 'byIARNo'):
		title = "Inspected deliveries by IAR Number"
		delivery = Delivery.objects.filter(date_inspected__isnull=False).filter(iar_no__contains=request.GET['IARNo']).order_by('date_inspected')
		return render(request, 'delivery_inspection/reports_base.html', {'reports':delivery, 'title':title})
	elif(request.GET['reportType'] == 'byPurpose'):
		title = "Inspected deliveries by Purpose"
		delivery = Delivery.objects.filter(date_inspected__isnull=False).filter(purpose__contains=request.GET['purposeKeywords']).order_by('date_inspected')
		return render(request, 'delivery_inspection/reports_base.html', {'reports':delivery, 'title':title})
	elif(request.GET['reportType'] == 'bySupplier'):
		title = "Inspected deliveries by Supplier"
		delivery = Delivery.objects.filter(date_inspected__isnull=False).filter(supplier__contains=request.GET['supplierKeywords']).order_by('date_inspected')
		return render(request, 'delivery_inspection/reports_base.html', {'reports':delivery, 'title':title})
	else:
		print("No report type selected")
		return render(request, 'delivery_inspection/reports.html', {'error':'No report selected or invalid parameter!'})
	

def reports(request):
	return render(request, 'delivery_inspection/reports.html')
		
def signupuser(request):
	if request.method == 'GET':
		return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm()})
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('inspection:alldeliveries')
			except IntegrityError:
				return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already bee taken. Please use a new username.'})
		else:
			return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm(), 'error':'Password did not match'})

def loginuser(request):
	if request.method == 'GET':
		return render(request, 'delivery_inspection/loginuser.html', {'form':LoginForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'delivery_inspection/loginuser.html', {'form':LoginForm(), 'error':'Username and Password did not match.'})
		else:
			login(request, user)
			return redirect('inspection:alldeliveries')

@login_required
def logoutuser(request):
	if request.method == 'POST':
		logout(request)
		return render(request, "delivery_inspection/logoutuser.html")

@login_required
def dashboard(request):
	return render(request, 'delivery_inspection/dashboard.html')


def is_inspector(request):
	user = User.objects.filter(is_staff=1)
	inspector = user.filter(username=request.user).exists()
	if inspector:
		return True;
	else:
		return False;

@login_required
def alldeliveries(request):
	delivery = Delivery.objects.filter(date_inspected__isnull=True) #show only not inspected deliveriess
	if is_inspector(request): #check if inspector or not
		print("go to inspector page!")
		return render(request, 'delivery_inspection/inspector_allpending.html', {'delivery':delivery})
	else:
		print("go to user page!")
		return render(request, 'delivery_inspection/allpending.html', {'delivery':delivery})

@login_required
def mydeliveries(request):
	delivery = Delivery.objects.filter(date_inspected__isnull=True, created_by_id=request.user) #show only not inspected deliveries
	return render(request, 'delivery_inspection/currentpending.html', {'delivery':delivery})

@login_required
def newdelivery(request):
	if request.method == 'GET':
		return render(request, 'delivery_inspection/newdelivery.html', {'form':DeliveryForm()})
	else:
		try:
			form = DeliveryForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.created_by = request.user #set created_by to the logged in user
			new.save()
			return redirect('inspection:mydeliveries')
		except ValueError:
			return render(request, 'delivery_inspection/newdelivery.html', {'form':DeliveryForm(), 'error':'Invalid data entered'})

@login_required
def viewdelivery(request, pk):
	delivery = get_object_or_404(Delivery, pk=pk, created_by_id=request.user) #can only edit by the creator
	#delivery = get_object_or_404(Delivery, pk=iar_no)
	if request.method == 'GET':
		form = DeliveryForm(instance=delivery)
		return render(request, 'delivery_inspection/viewdelivery.html', {'delivery':delivery, 'form':form})
	else:
		try:
			form = DeliveryForm(request.POST, request.FILES, instance=delivery)
			#print(form)
			form.save()
			return redirect('inspection:mydeliveries')
		except ValueError:
			return render(request, 'delivery_inspection/viewdelivery.html', {'delivery':delivery, 'form':form, 'error':'Invalid data entered'})	

@login_required
def deletedelivery(request, pk):
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'POST':
		delivery.delete()
		return redirect('inspection:mydeliveries')

#overall CRUD
# @login_required
# def inspectorviewdelivery(request, pk):
# 	delivery = get_object_or_404(Delivery, pk=pk)
# 	if request.method == 'GET':
# 		form = DeliveryForm(instance=delivery)
# 		return render(request, 'delivery_inspection/inspector_viewdelivery.html', {'delivery':delivery, 'form':form})	
# 	else:
# 		try:
# 			form = DeliveryForm(request.POST, instance=delivery)
# 			form.save()
# 			return redirect('inspection:alldeliveries')
# 		except ValueError:
# 			return render(request, 'delivery_inspection/inspector_viewdelivery.html', {'delivery':delivery, 'form':form, 'error':'Invalid data entered'})	




@login_required
def inspectorviewdelivery(request, pk):
	delivery = Delivery.objects.filter(pk=pk)
	#print(delivery)
	return render(request, 'delivery_inspection/inspector_viewdelivery.html', {'delivery':delivery})

@login_required
def inspectdelivery(request, pk):
	print("inside inspectdelivery")
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'POST':
		delivery.inspected_by = str(request.user)
		delivery.date_inspected = timezone.now()
		delivery.save()
		return redirect('inspection:alldeliveries')

@login_required
def inspecteddelivery(request):
	delivery = Delivery.objects.filter(date_inspected__isnull=False).order_by('-date_inspected') #will show inspected recently
	return render(request, 'delivery_inspection/inspected.html', {'delivery':delivery})

def deleteimage(request, pk):
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'POST':
		print("delete image")
		if delivery.image:
			delivery.image.delete()
	return redirect('inspection:viewdelivery', pk=pk)

def viewinspected(request, pk):
	delivery = Delivery.objects.filter(pk=pk)
	return render(request, 'delivery_inspection/viewinspected.html', {'delivery':delivery})