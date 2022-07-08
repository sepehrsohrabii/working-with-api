from django.contrib import admin
from django.urls import path, include
from search_data import views

urlpatterns = [
    path('', views.save_search_data)
]
