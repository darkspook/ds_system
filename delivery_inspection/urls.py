from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'inspection'

urlpatterns = [
    path('', views.home, name='home'),
    
    # Inspection
    # path('dashboard/', views.dashboard, name='dashboard'),
   	path('newdeliveries/', views.newdeliveries, name='newdeliveries'),
   	# path('alldeliveries/', views.alldeliveries, name='alldeliveries'),
   	path('mydeliveries/', views.mydeliveries, name='mydeliveries'),
    path('view/<int:pk>', views.viewdelivery, name='viewdelivery'),
    path('view/<int:pk>/delete', views.deletedelivery, name='deletedelivery'),
   	path('completed/', views.completeddelivery, name='completeddelivery'),
    path('view/<int:pk>/deleteimage', views.deleteimage, name='deleteimage'),
    path('view/<int:pk>/inspected', views.viewinspected, name='viewinspected'),
    path('reports/', views.reports, name='reports'),
    path('generatereport/', views.generate_report, name='generate_report'),

    # Inspector views
    path('inspectorview/<int:pk>', views.inspectorviewdelivery, name='inspectorviewdelivery'), # home interface with clickable IAR No.
    path('view/<int:pk>/inspectdelivery', views.inspectdelivery, name='inspectdelivery'), # Inspect & Accept button/POST
    path('view/<int:pk>/inspectpartialdelivery', views.inspectpartialdelivery, name='inspectpartialdelivery'),
    path('view/<int:pk>/deletepartialdelivery', views.deletepartialdelivery, name='deletepartialdelivery'),
   	# Auth
    # path('signup/', views.signupuser, name='signupuser'),
    # path('login/', views.loginuser, name='loginuser'),
    # path('logout/', views.logoutuser, name='logoutuser'),

    #Test
    path('test/', views.test, name='test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
