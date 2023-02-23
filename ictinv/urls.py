from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    AssetListView,
    AssetAvailableListView,
    AssetDetailView, 
    AssetCreateView, 
    AssetUpdateView, 
    AssetDeleteView,
    ComponentListView,
    ComponentAvailableListView,
    ComponentDetailView,
    ComponentCreateView,
    ComponentDeleteView,
    EndUserCreateView,
    EndUserListView,
    EndUserUpdateView,
    EndUserDeleteView,
    AssetTypeCreateView,
    AssetTypeListView,
    AssetTypeUpdateView,
    AssetTypeDeleteView,
    BrandCreateView,
    BrandListView,
    BrandUpdateView,
    BrandDeleteView,
    LocationCreateView,
    LocationListView,
    LocationUpdateView,
    LocationDeleteView,
    )

app_name = 'ictinv'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('asset/', AssetListView.as_view(), name='asset_list'),
    path('asset/available', AssetAvailableListView.as_view(), name='asset_available_list'),
    path('asset/<int:pk>/', AssetDetailView.as_view(), name='asset_detail'),
    path('asset/<int:pk>/update/', AssetUpdateView.as_view(), name='asset_update'),
    path('asset/<int:pk>/delete/', AssetDeleteView.as_view(), name='asset_delete'),
    path('asset/<int:pk>/deleteimage/', views.delete_image, name='delete_image'),
    path('asset/new/', AssetCreateView.as_view(), name='asset_create'),
    path('asset/<int:pk>/clone/', views.asset_clone, name='asset_clone'),
    path('component/', ComponentListView.as_view(), name='component_list'),
    path('component/available', ComponentAvailableListView.as_view(), name='component_available_list'),
    path('component/<int:pk>', ComponentDetailView.as_view(), name='component_detail'),
    path('component/new/', ComponentCreateView.as_view(), name='component_create'),
    path('component/<int:pk>/add/', views.component_add, name='component_add'),
    path('component/<int:pk>/view/', views.component_listview, name='component_listview'),
    path('component/<int:pk>/update/', views.component_updateview, name='component_update'),
    path('component/<int:pk>/update2/', views.component_updateview, name='component_update2'),
    path('component/<int:pk>/deleteimage/', views.component_delete_image, name='component_delete_image'),
    # path('component/<int:pk>/delete/', views.component_deleteview, name='component_delete'),
    path('component/<int:pk>/delete/', ComponentDeleteView.as_view(), name='component_delete'),
    path('component/<int:pk>/clone/', views.component_clone, name='component_clone'),
    path('component/<int:pk>/clone2/', views.component_clone, name='component_clone2'),
    
    # Setup
    path('enduser/new/', EndUserCreateView.as_view(), name='enduser_create'),
    path('enduser/', EndUserListView.as_view(), name='enduser_list'),
    path('enduser/<int:pk>/update/', EndUserUpdateView.as_view(), name='enduser_update'),
    path('enduser/<int:pk>/delete/', EndUserDeleteView.as_view(), name='enduser_delete'),
    path('assettype/new/', AssetTypeCreateView.as_view(), name='assettype_create'),
    path('assettype/', AssetTypeListView.as_view(), name='assettype_list'),
    path('assettype/<int:pk>/update/', AssetTypeUpdateView.as_view(), name='assettype_update'),
    path('assettype/<int:pk>/delete/', AssetTypeDeleteView.as_view(), name='assettype_delete'),
    path('brand/new/', BrandCreateView.as_view(), name='brand_create'),
    path('brand/', BrandListView.as_view(), name='brand_list'),
    path('brand/<int:pk>/update/', BrandUpdateView.as_view(), name='brand_update'),
    path('brand/<int:pk>/delete/', BrandDeleteView.as_view(), name='brand_delete'),
    path('location/new/', LocationCreateView.as_view(), name='location_create'),
    path('location/', LocationListView.as_view(), name='location_list'),
    path('location/<int:pk>/update/', LocationUpdateView.as_view(), name='location_update'),
    path('location/<int:pk>/delete/', LocationDeleteView.as_view(), name='location_delete'),


    #Test
    path('test/', views.test, name='test'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
