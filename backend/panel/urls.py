from django.contrib import admin
from django.urls import path, include
from panel import views

urlpatterns = [
    path('', views.AdminPanel, name='AdminPanel')
]
