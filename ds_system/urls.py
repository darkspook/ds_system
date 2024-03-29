"""ds_system URL Configuration 

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from ictinv import views
from delivery_inspection import views
from portfolio import views
from users import views as user_views
from django.contrib.auth import views as auth_views
from users.decorators import unauthenticated_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', unauthenticated_user(auth_views.LoginView.as_view(template_name='users/login.html')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('welcome/', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('tree/', views.tree, name='tree'),
    path('inspection/', include('delivery_inspection.urls')),
    path('accounts/', include('users.urls')),
    path('ictinv/', include('ictinv.urls')),
    path('ictrequest/', include('ictrequest.urls')),
    path('risgen/', include('risgen.urls')),

    path('duty/', views.dutygenerator, name='dutygenerator'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)