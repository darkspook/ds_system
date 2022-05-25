from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import (
    AssetListView, 
    AssetDetailView, 
    AssetCreateView, 
    AssetUpdateView, 
    AssetDeleteView, 
    ComponentCreateView,
    ComponentDeleteView,
    )

app_name = 'ict_inventory'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('asset/', AssetListView.as_view(), name='asset_list'),
    path('asset/<int:pk>/', AssetDetailView.as_view(), name='asset_detail'),
    path('asset/<int:pk>/update/', AssetUpdateView.as_view(), name='asset_update'),
    path('asset/<int:pk>/delete/', AssetDeleteView.as_view(), name='asset_delete'),
    path('asset/<int:pk>/deleteimage/', views.delete_image, name='delete_image'),
    path('asset/new/', AssetCreateView.as_view(), name='asset_create'),
    path('asset/<int:pk>/clone/', views.asset_clone, name='asset_clone'),
    path('component/new/', ComponentCreateView.as_view(), name='component_create'),
    path('component/<int:pk>/add/', views.component_add, name='component_add'),
    path('component/<int:pk>/view/', views.component_listview, name='component_listview'),
    path('component/<int:pk>/update/', views.component_updateview, name='component_update'),
    path('component/<int:pk>/deleteimage/', views.component_delete_image, name='component_delete_image'),
    # path('component/<int:pk>/delete/', views.component_deleteview, name='component_delete'),
    path('component/<int:pk>/delete/', ComponentDeleteView.as_view(), name='component_delete'),
    path('component/<int:pk>/clone/', views.component_clone, name='component_clone'),
    path('login/', auth_views.LoginView.as_view(template_name='ict_inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='ict_inventory/login.html'), name='logout'),

    #Test
    path('test/', views.test, name='test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
