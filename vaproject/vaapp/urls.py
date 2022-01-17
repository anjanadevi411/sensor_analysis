from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload_csv, name='upload_csv'),
    path('display/<int:id>', views.display, name='dispaly'),
]