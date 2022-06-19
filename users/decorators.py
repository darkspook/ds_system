from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

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
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				raise PermissionDenied
				#return HttpResponse('Your are not authorized to view this page.')
		return wrapper_func
	return decorator
