from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import DeliveryForm, PartialDeliveryForm
from .models import Delivery, PartialDelivery
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import datetime
import datetime, math
from users.decorators import allowed_users
from django.contrib import messages


def reset_confirm(request, pk):
		delivery = get_object_or_404(Delivery, pk=pk)
		yearmonth = str(delivery)[:-3]
		newiarno = yearmonth + "001"
		delivery.iar_no = newiarno
		delivery.save()
		messages.success(request, f'IAR No. reset successfully!')

		return redirect('inspection:home')

# @login_required
@allowed_users(allowed_roles=['diainspector'])
def reset_iarno(request):
	last_record = Delivery.objects.last()
	pk=last_record.pk
	page_title = 'Reset IAR No.'
	delivery = Delivery.objects.filter(pk=pk)
	context = {
		'delivery':delivery,
		'pk':pk,
		'title':page_title,
	}
	return render(request, 'delivery_inspection/inspector_resetiarno.html', context)

def generatemultichart(request, year):
	# print("Year: ", year)
	t = ()
	for i in range(1,13):
		count = Delivery.objects.filter(date_inspected__month=i, date_inspected__year=year).count()
		t += count,
	data = str(t)[1:-1]
	maxval = round(max(t)/10)*10
	return data, maxval+5

@login_required
@allowed_users(allowed_roles=['diainspector', 'diauser'])
def home(request):
	page_title = 'Dashboard'
	delivery = Delivery.objects.filter(date_inspected__isnull=True) #show only not inspected deliveriess
	current_year = datetime.datetime.now().year
	last_year = current_year - 1
	two_years_ago = current_year - 2
	data1, maxval1 = generatemultichart(request, current_year) #year 0
	data2, maxval2 = generatemultichart(request, last_year) #year -1
	data3, maxval3 = generatemultichart(request, two_years_ago) #year -2
	# data1, maxval1 = generatechart(request) #year 0
	# data2, maxval2 = generatechart(request) #year -1
	# data3, maxval3 = generatechart(request) #year -2
	context = {'delivery':delivery, 'data1':data1, 'maxval1':maxval1, 'year1':str(current_year), 'data2':data2, 'maxval2':maxval2, 'year2':str(last_year), 'data3':data3, 'maxval3':maxval3, 'year3':str(two_years_ago), 'title':page_title,}
	if is_inspector(request): #check if inspector or not
		print("go to inspector page!")
		return render(request, 'delivery_inspection/inspector_allpending.html', context)
	else:
		print("go to user page!")
		return render(request, 'delivery_inspection/allpending.html', context)

def generate_report(request):
	if request.GET['reportType'] == 'dateRange':
		dateFrom = request.GET['dateFrom']
		dateTo = request.GET['dateTo'] 
		if not dateFrom or not dateTo:
			return render(request, 'delivery_inspection/reports_base.html', {'title':'No parameter provided'})
		else:
			dateFromf = datetime.datetime.strptime(dateFrom, '%Y-%m-%d').strftime("%b. %d, %Y")
			print(dateFromf)
			dateTof = datetime.datetime.strptime(dateTo, '%Y-%m-%d').strftime("%b. %d, %Y")
			print(dateTof)
			title = "By Date Range: {} to {}".format(dateFromf, dateTof)
			# delivery = Delivery.objects.filter(date_inspected__isnull=False).order_by('date_inspected')
			delivery = Delivery.objects.filter(date_inspected__isnull=False).exclude(date_delivered__gte=dateTo).filter(date_delivered__gte=dateFrom).order_by('iar_no')
			return render(request, 'delivery_inspection/reports_base.html', {'reports':delivery, 'title':title})
	elif(request.GET['reportType'] == 'byIARNo'):
		title = 'By IAR Number "'+request.GET['IARNo']+'"'
		delivery = Delivery.objects.filter(date_inspected__isnull=False).filter(iar_no__contains=request.GET['IARNo']).order_by('iar_no')
		return render(request, 'delivery_inspection/reports_base.html', {'reports':delivery, 'title':title})
	elif(request.GET['reportType'] == 'byPurpose'):
		title = 'By Purpose "'+request.GET['purposeKeywords']+'"'
		delivery = Delivery.objects.filter(date_inspected__isnull=False).filter(purpose__icontains=request.GET['purposeKeywords']).order_by('iar_no')
		return render(request, 'delivery_inspection/reports_base.html', {'reports':delivery, 'title':title})
	elif(request.GET['reportType'] == 'bySupplier'):
		#title = "By Supplier"
		title = 'By Supplier "'+request.GET['supplierKeywords']+'"'
		delivery = Delivery.objects.filter(date_inspected__isnull=False).filter(supplier__icontains=request.GET['supplierKeywords']).order_by('iar_no')
		return render(request, 'delivery_inspection/reports_base.html', {'reports':delivery, 'title':title})
	else:
		# print("No report type selected")
		return render(request, 'delivery_inspection/reports.html', {'error':'No report selected or invalid parameter!'})
	
# @login_required
@allowed_users(allowed_roles=['diainspector', 'diauser'])
def reports(request):
	page_title = 'Reports'
	return render(request, 'delivery_inspection/reports.html', {'title':page_title,})

# @login_required
# def dashboard(request):
# 	return render(request, 'delivery_inspection/dashboard.html')

def is_inspector(request):
	user = User.objects.filter(is_staff=1)
	inspector = user.filter(username=request.user).exists()
	if inspector:
		return True;
	else:
		return False;

# @login_required
@allowed_users(allowed_roles=['diainspector', 'diauser'])
def mydeliveries(request):
	page_title = 'My Deliveries'
	delivery = Delivery.objects.filter(date_inspected__isnull=True, created_by_id=request.user).order_by('-date_delivered') #show only not inspected deliveries
	return render(request, 'delivery_inspection/mydeliveries.html', {'delivery':delivery, 'title':page_title,})

# @login_required
@allowed_users(allowed_roles=['diainspector', 'diauser'])
def newdeliveries(request):
	page_title = 'New Deliveries'
	if request.method == 'GET':
		return render(request, 'delivery_inspection/newdeliveries.html', {'form':DeliveryForm(), 'title':page_title,})
	else:
		try:
			form = DeliveryForm(request.POST, request.FILES)
			new = form.save(commit=False) #will not save to DB
			new.created_by = request.user #set created_by to the logged in user
			new.save()
			return redirect('inspection:mydeliveries')
		except ValueError:
			return render(request, 'delivery_inspection/newdeliveries.html', {'form':DeliveryForm(), 'error':'Invalid data entered', 'title':page_title,})

# @login_required
@allowed_users(allowed_roles=['diainspector', 'diauser'])
def viewdelivery(request, pk):
	page_title = 'Update Delivery'
	delivery = get_object_or_404(Delivery, pk=pk, created_by_id=request.user) #can only edit by the creator
	#delivery = get_object_or_404(Delivery, pk=iar_no)
	if request.method == 'GET':
		form = DeliveryForm(instance=delivery)
		return render(request, 'delivery_inspection/viewdelivery.html', {'delivery':delivery, 'form':form, 'title':page_title,})
	else:
		try:
			form = DeliveryForm(request.POST, request.FILES, instance=delivery)
			#print(form)
			form.save()
			return redirect('inspection:mydeliveries')
		except ValueError:
			return render(request, 'delivery_inspection/viewdelivery.html', {'delivery':delivery, 'form':form, 'error':'Invalid data entered', 'title':page_title,})	

# @login_required
@allowed_users(allowed_roles=['diainspector', 'diauser'])
def deletedelivery(request, pk):
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'POST':
		delivery.delete()
		return redirect('inspection:mydeliveries')

# @login_required
@allowed_users(allowed_roles=['diainspector'])
def inspectorviewdelivery(request, pk):
	page_title = 'Inspect & Accept Delivery'
	delivery = Delivery.objects.filter(pk=pk)
	partialdelveries = PartialDelivery.objects.filter(delivery_id=pk)
	context = {
		'partialdelveries':partialdelveries,
		'delivery':delivery,
		'pk':pk,
		'title':page_title,
	}
	return render(request, 'delivery_inspection/inspector_viewdelivery.html', context)

# @login_required
@allowed_users(allowed_roles=['diainspector', 'diauser'])
def inspectdelivery(request, pk):
	# print("inside inspectdelivery")
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'POST':
		delivery.inspected_by = str(request.user)
		delivery.date_inspected = timezone.now()
		delivery.save()
		return redirect('inspection:home')

@allowed_users(allowed_roles=['diainspector'])
def inspectpartialdelivery(request, pk):
	print("inside inspectpartialdelivery")
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'GET':
		form = PartialDeliveryForm()
		context = {
			'form':form,
			'delivery':delivery,
		}
		return render(request, 'delivery_inspection/inspector_partialdelivery.html', context)
	else:
		try:
			form = PartialDeliveryForm(request.POST)
			new = form.save(commit=False) #will not save to DB
			new.delivery_id = pk
			new.inspected_by = request.user
			new.save()
			messages.success(request, f'Partial Inspection added successfully!')
			return redirect('inspection:inspectorviewdelivery', pk)
		except ValueError:
		# except ValueError as e:
			# print(e)
			return render(request, 'delivery_inspection/inspector_partialdelivery.html', {'form':form, 'error':'Invalid data entered'})
		return redirect('inspection:inspectorviewdelivery', pk)

def deletepartialdelivery(request, pk):
	pdelivery = get_object_or_404(PartialDelivery, pk=pk)
	if request.method == 'POST':
		pdelivery.delete()
		messages.success(request, f'Partial Inspection deleted successfully!')
		return redirect('inspection:inspectorviewdelivery', pdelivery.delivery_id)

# @login_required
@allowed_users(allowed_roles=['diainspector', 'diauser'])
def completeddelivery(request):
	page_title = 'Completed Deliveries'
	delivery = Delivery.objects.filter(date_inspected__isnull=False).order_by('-date_inspected') #will show inspected recently
	context = {
		'delivery' : delivery,
		'title':page_title,
	}
	return render(request, 'delivery_inspection/completed.html', context)

def deleteimage(request, pk):
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'POST':
		# print("delete image")
		if delivery.image:
			delivery.image.delete()
	return redirect('inspection:viewdelivery', pk=pk)

@allowed_users(allowed_roles=['diainspector', 'diauser'])
def viewinspected(request, pk):
	page_title = 'Completed Delivery'
	delivery = Delivery.objects.filter(pk=pk)
	partialdelveries = PartialDelivery.objects.filter(delivery_id=pk)
	context = {
		'partialdelveries':partialdelveries,
		'delivery':delivery,
		'title':page_title,
	}
	return render(request, 'delivery_inspection/viewinspected.html', context)

def generatechart(request):
	t = ()
	for i in range(1,13):
		count = Delivery.objects.filter(date_inspected__month=i).count()
		t += count,
	data = str(t)[1:-1]
	maxval = round(max(t)/10)*10
	return data, maxval+5

def test(request):
	t = ()
	for i in range(1,13):
		count = Delivery.objects.filter(date_inspected__month=i).count()
		t += count,
	data = str(t)[1:-1]
	maxval = round(max(t)/10)*10
	print(maxval)
	return render(request, 'delivery_inspection/test.html', {'data':data, 'maxval':maxval+5})

# @login_required
# @allowed_users(allowed_roles=['inspector'])
# def alldeliveries(request):
# 	delivery = Delivery.objects.filter(date_inspected__isnull=True) #show only not inspected deliveriess
# 	data, maxval = generatechart(request)
# 	context = {'delivery':delivery, 'data':data, 'maxval':maxval}
# 	if is_inspector(request): #check if inspector or not
# 		print("go to inspector page!")
# 		return render(request, 'delivery_inspection/inspector_allpending.html', context)
# 	else:
# 		print("go to user page!")
# 		return render(request, 'delivery_inspection/allpending.html', context)

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

# def signupuser(request):
# 	if request.method == 'GET':
# 		return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm()})
# 	else:
# 		if request.POST['password1'] == request.POST['password2']:
# 			try:
# 				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
# 				user.save()
# 				login(request, user)
# 				return redirect('inspection:alldeliveries')
# 			except IntegrityError:
# 				return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already bee taken. Please use a new username.'})
# 		else:
# 			return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm(), 'error':'Password did not match'})

# def loginuser(request):
# 	if request.method == 'GET':
# 		return render(request, 'delivery_inspection/loginuser.html', {'form':LoginForm()})
# 	else:
# 		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
# 		if user is None:
# 			return render(request, 'delivery_inspection/loginuser.html', {'form':LoginForm(), 'error':'Username and Password did not match.'})
# 		else:
# 			login(request, user)
# 			return redirect('inspection:alldeliveries')

# # @login_required
# def logoutuser(request):
# 	if request.method == 'POST':
# 		logout(request)
# 		return render(request, "delivery_inspection/logoutuser.html")