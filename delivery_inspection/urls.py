from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'inspection'

urlpatterns = [
    path('', views.loginuser, name='loginuser'),
    
    # Inspection
    path('dashboard/', views.dashboard, name='dashboard'),
   	path('newdelivery/', views.newdelivery, name='newdelivery'),
   	path('alldeliveries/', views.alldeliveries, name='alldeliveries'),
   	path('mydeliveries/', views.mydeliveries, name='mydeliveries'),
    path('view/<int:pk>', views.viewdelivery, name='viewdelivery'),
    path('view/<int:pk>/inspect', views.inspectdelivery, name='inspectdelivery'),
    path('view/<int:pk>/delete', views.deletedelivery, name='deletedelivery'),
   	path('accepted/', views.inspecteddelivery, name='inspecteddelivery'),

    # Inspector views
    path('inspectorview/<int:pk>', views.inspectorviewdelivery, name='inspectorviewdelivery'),

   	# Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)