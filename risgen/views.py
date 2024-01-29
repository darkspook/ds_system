from django.shortcuts import render, redirect, get_object_or_404
from .models import IssuingRIS, CompletedDIA, IssuingRISItems
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import IssuingRISItemsForm, IssuingRISForm
from django.contrib import messages
from django.utils import timezone

# def issuingris_new(request):

# 	return pass

def issuedris_detail(request, pk):
	page_title = 'Issued RIS Detail'
	issuingris = IssuingRIS.objects.filter(pk=pk)
	issuingrisitems = IssuingRISItems.objects.filter(ris_no_id=pk)
	context = {
		'issuingris':issuingris,
		'issuingrisitems':issuingrisitems,
		'pk':pk,
		'title':page_title,
	}
	return render(request, 'risgen/issuedris_detail.html', context)

def issuedris_list(request):
	risno = IssuingRIS.objects.filter(date_issued__isnull=False)
	context = {'ris_no':risno}
	# context = {}
	# print('context = ', context);
	return render(request, 'risgen/issuedris_list.html', context)

def issue_ris(request, pk):
	issuingris = get_object_or_404(IssuingRIS, pk=pk)
	if request.method == 'POST':
		issuingris.date_issued = timezone.now()
		issuingris.save()
		messages.success(request, f'RIS and Items issued successfully!')
		return redirect('risgen:home')

def generate_rislip(request, pk):
	page_title = 'RIS'
	issuingris = IssuingRIS.objects.filter(pk=pk)
	issuingrisitems = IssuingRISItems.objects.filter(ris_no_id=pk)
	context = {
		'issuingris':issuingris,
		'issuingrisitems':issuingrisitems,
		'pk':pk,
		'title':page_title,
	}
	return render(request, 'risgen/reports_base.html', context)

def item_delete(request, pk):
	issuingrisitems = get_object_or_404(IssuingRISItems, pk=pk)
	if request.method == 'POST':
		issuingrisitems.delete()
		messages.success(request, f'Item deleted successfully!')
		return redirect('risgen:issuingris_detail', issuingrisitems.ris_no_id)

def item_update(request, pk):
	page_title = 'Edit Item'
	issuingrisitems = get_object_or_404(IssuingRISItems, pk=pk)
	if request.method == 'GET':
		form = IssuingRISItemsForm(instance=issuingrisitems)
		return render(request, 'risgen/item_update.html', {'issuingrisitems':issuingrisitems, 'form':form, 'title':page_title})
	else:
		try:
			form = IssuingRISItemsForm(request.POST, request.FILES, instance=issuingrisitems)
			form.save()
			messages.success(request, 'Item was updated successfully.')
			return redirect('risgen:issuingris_detail', issuingrisitems.ris_no_id)
		except ValueError:
			messages.error(request, 'Invalid data entered.')
			return render(request, 'risgen/item_update.html', {'issuingrisitems':issuingrisitems, 'form':form})

def home(request):
	CompletedDIA.get_completed_dia_init()
	# CompletedDIA.get_completed_dia()
	# print(completed_dia)
	IssuingRIS.assign_ris_no()
	ris_no = IssuingRIS.generate_ris_no()
	risno = IssuingRIS.objects.filter(date_issued__isnull=True)
	context = {'ris_no':risno}
	# context = {}
	# print('context = ', context);
	return render(request, 'risgen/home.html', context)

def item_add(request, pk):
	"""Add Item"""
	page_title = 'Add Item'
	issuingris = get_object_or_404(IssuingRIS, pk=pk)
	init_val_stock_no = issuingris.issuingrisitems_set.all().count()+1
	form = IssuingRISItemsForm(initial={'stock_no':init_val_stock_no,})
	# form = IssuingRISItemsForm()
	context = {
			'issuingris':issuingris,
			'form':form,
			'title':page_title
		}
	if request.method == 'GET':
		return render(request, 'risgen/item_add.html', context)
	else:
		try:
			form = IssuingRISItemsForm(request.POST)
			new = form.save(commit=False) #will not save to DB
			new.ris_no_id = pk
			new.save()
			messages.success(request, 'Item was added successfully.')
			return redirect('risgen:issuingris_detail', pk)
		except ValueError:
			messages.error(request, 'Invalid data entered.')
			return render(request, 'risgen/item_add.html', {'form':IssuingRISItemsForm()})

class PageTitleMixin:
	title = ""
	def get_title(self):
		return self.title
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		title = self.get_title()
		if not title:
			raise ValueError("Page title should not be empty")
		context["title"] = title
		return context

class IssuingRISCreateView(SuccessMessageMixin, PageTitleMixin, CreateView):
	"""Generic creating view for Issuing RIS
	This is New Issuing RIS in navigation"""
	model = IssuingRIS
	template_name = 'risgen/issuingris_new.html'
	title = "New Issuing RIS"
	form_class = IssuingRISForm
	success_message = "Issuing RIS was created successfully"

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class IssuingRISItemsCreateView(SuccessMessageMixin, PageTitleMixin, CreateView):
	"""Generic creating view for IssuingRISItems
	This is in navigation"""
	model = IssuingRISItems
	template_name = 'ictinv/issuingrisitems_new.html'
	form_class = IssuingRISItemsForm
	title = "Add RIS Items"
	success_message = "Item was created successfully"

# class IssuingRISDetailView(PageTitleMixin, DetailView):
# 	"""Generic detail view for IssuingRIS"""
# 	model = IssuingRIS
# 	title = "Issuing RIS Detail"

# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)

def issuingris_detail(request, pk):
	page_title = 'Issuing RIS Detail'
	issuingris = IssuingRIS.objects.filter(pk=pk)
	issuingrisitems = IssuingRISItems.objects.filter(ris_no_id=pk)
	context = {
		'issuingris':issuingris,
		'issuingrisitems':issuingrisitems,
		'pk':pk,
		'title':page_title,
	}
	return render(request, 'risgen/issuingris_detail.html', context)

def reset_ris_no_series():
	pass
