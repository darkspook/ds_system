from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import (IssuingRISCreateView)

app_name = 'risgen'

urlpatterns = [
    path('', views.home, name='home'),
    # path('risno/<int:pk>/', IssuingRISDetailView.as_view(), name='issuingris_detail'),
    path('risno/<int:pk>/', views.issuingris_detail, name='issuingris_detail'),
    path('risno/<int:pk>/additem/', views.item_add, name='item_add'),
    path('risno/<int:pk>/updateitem/', views.item_update, name='item_update'),
    path('risno/<int:pk>/deleteitem', views.item_delete, name='item_delete'),
    path('risno/<int:pk>/rislip', views.generate_rislip, name='generate_rislip'),
    path('risno/<int:pk>/issueris', views.issue_ris, name='issue_ris'),
    path('issuedris', views.issuedris_list, name='issuedris_list'),
    path('risno/<int:pk>/issuedris', views.issuedris_detail, name='issuedris_detail'),
    # path('ris/new', views.issuingris_new, name='issuingris_new'),
    path('ris/new', IssuingRISCreateView.as_view(), name='issuingris_new'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
