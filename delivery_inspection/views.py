from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import DeliveryForm
from .models import Delivery
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import datetime

#def home(request):
#	return render(request, 'delivery_inspection/home.html')

def signupuser(request):
	if request.method == 'GET':
		return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm()})
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('inspection:dashboard')
			except IntegrityError:
				return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already bee taken. Please use a new username.'})
		else:
			return render(request, 'delivery_inspection/signupuser.html', {'form':UserCreationForm(), 'error':'Password did not match'})

def loginuser(request):
	if request.method == 'GET':
		return render(request, 'delivery_inspection/loginuser.html', {'form':AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'delivery_inspection/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match.'})
		else:
			login(request, user)
			return redirect('inspection:dashboard')

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

# def is_member(user):
# 	print("Inspector? "+str(user.groups.filter(name='Inspector').exists()))
# 	return user.groups.filter(name='Inspector').exists()

@login_required
def allpending(request):
	delivery = Delivery.objects.filter(date_inspected__isnull=True) #show only not inspected deliveries
	if is_inspector(request): #check if inspector or not
		print("go to inspector page!")
		return render(request, 'delivery_inspection/inspector_allpending.html', {'delivery':delivery})
	else:
		print("go to user page!")
		return render(request, 'delivery_inspection/allpending.html', {'delivery':delivery})

@login_required
def mypending(request):
	delivery = Delivery.objects.filter(date_inspected__isnull=True, created_by_id=request.user) #show only not inspected deliveries
	return render(request, 'delivery_inspection/currentpending.html', {'delivery':delivery})

@login_required
def newdelivery(request):
	if request.method == 'GET':
		return render(request, 'delivery_inspection/newdelivery.html', {'form':DeliveryForm()})
	else:
		try:
			form = DeliveryForm(request.POST)
			new = form.save(commit=False) #will not save to DB
			new.created_by = request.user #set created_by to the logged in user
			new.save()
			return redirect('inspection:dashboard')
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
			form = DeliveryForm(request.POST, instance=delivery)
			form.save()
			return redirect('inspection:mypending')
		except ValueError:
			return render(request, 'delivery_inspection/viewdelivery.html', {'delivery':delivery, 'form':form, 'error':'Invalid data entered'})	

@login_required
#@user_passes_test(is_member) #validate if inspector
def inspectdelivery(request, pk):
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'POST':
		delivery.inspected = 1
		delivery.inspected_by = str(request.user)
		delivery.date_inspected = timezone.now()
		delivery.save()
		return redirect('inspection:mypending')

@login_required
def deletedelivery(request, pk):
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'POST':
		delivery.delete()
		return redirect('inspection:mypending')

@login_required
def inspecteddelivery(request):
	delivery = Delivery.objects.filter(date_inspected__isnull=False).order_by('-date_inspected') #will show inspected recently
	return render(request, 'delivery_inspection/inspected.html', {'delivery':delivery})

@login_required
def inspectorviewdelivery(request, pk):
	delivery = get_object_or_404(Delivery, pk=pk)
	if request.method == 'GET':
		form = DeliveryForm(instance=delivery)
		return render(request, 'delivery_inspection/viewdelivery.html', {'delivery':delivery, 'form':form})	
	else:
		try:
			form = DeliveryForm(request.POST, instance=delivery)
			form.save()
			return redirect('inspection:allpending')
		except ValueError:
			return render(request, 'delivery_inspection/viewdelivery.html', {'delivery':delivery, 'form':form, 'error':'Invalid data entered'})	


