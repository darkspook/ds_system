from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

# if user is already authenticated then send to home
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('users:home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

# if logged-in user is not part of a group raise http 403, access denied
def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			# group = None
			usrgrplist = []
			if request.user.groups.exists():
				# group = request.user.groups.all()[0].name
				usrgrplist = list(request.user.groups.values_list('name',flat = True))  

			print('User groups: ',usrgrplist)

			for i in allowed_roles:
				# if group in allowed_roles:
				if i in usrgrplist:
					return view_func(request, *args, **kwargs)
				else:
					#raise PermissionDenied
					#return HttpResponse('We\'re sorry, but you do not have access to this app.')
					return render(request, 'users/403.html')
		return wrapper_func
	return decorator
