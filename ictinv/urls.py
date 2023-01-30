from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    AssetListView, 
    AssetDetailView, 
    AssetCreateView, 
    AssetUpdateView, 
    AssetDeleteView, 
    ComponentCreateView,
    ComponentDeleteView,
    EndUserCreateView,
    EndUserListView,
    EndUserUpdateView,
    AssetTypeCreateView,
    AssetTypeListView,
    AssetTypeUpdateView,
    AssetTypeDeleteView,
    EndUserDeleteView,
    )

app_name = 'ictinv'

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
    
    # Setup
    path('enduser/new/', EndUserCreateView.as_view(), name='enduser_create'),
    path('enduser/', EndUserListView.as_view(), name='enduser_list'),
    path('enduser/<int:pk>/update/', EndUserUpdateView.as_view(), name='enduser_update'),
    path('enduser/<int:pk>/delete/', EndUserDeleteView.as_view(), name='enduser_delete'),
    path('assettype/new/', AssetTypeCreateView.as_view(), name='assettype_create'),
    path('assettype/', AssetTypeListView.as_view(), name='assettype_list'),
    path('assettype/<int:pk>/update/', AssetTypeUpdateView.as_view(), name='assettype_update'),
    path('assettype/<int:pk>/delete/', AssetTypeDeleteView.as_view(), name='assettype_delete'),

    #Test
    path('test/', views.test, name='test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
