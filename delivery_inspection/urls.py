from django.contrib import admin
from django.urls import path
from . import views

app_name = 'inspection'

urlpatterns = [
	path('', views.loginuser, name='loginuser'),
    
    # Inspection
    path('dashboard/', views.dashboard, name='dashboard'),
   	path('new/', views.newdelivery, name='newdelivery'),
   	path('allpending/', views.allpending, name='allpending'),
   	path('mypending/', views.mypending, name='mypending'),
    path('view/<int:pk>', views.viewdelivery, name='viewdelivery'),
    path('view/<int:pk>/inspect', views.inspectdelivery, name='inspectdelivery'),
    path('view/<int:pk>/delete', views.deletedelivery, name='deletedelivery'),
   	path('inspected/', views.inspecteddelivery, name='inspecteddelivery'),

    # Inspector views
    path('inspectorview/<int:pk>', views.inspectorviewdelivery, name='inspectorviewdelivery'),

   	# Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

]