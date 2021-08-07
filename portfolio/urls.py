from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

app_name = 'portfolio'

urlpatterns = [
    path('update/<int:pk>', views.SiteUpdate.as_view(), name='siteupdate'),
    path('delete/<int:pk>', views.SiteDelete.as_view(), name='sitedelete'),
    path('create/', views.siteCreate, name='sitecreate'),
]
