from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'ict_inventory'

urlpatterns = [
    path('', views.home, name='home'),
    path('newasset/', views.asset_new, name='asset_new'),
    path('newcomponent/', views.component_new, name='component_new'),
    path('detail/<int:pk>/', views.asset_detail, name='asset_detail'),

    #Test
    path('test/', views.test, name='test'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
