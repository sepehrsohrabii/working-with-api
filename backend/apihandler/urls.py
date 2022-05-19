from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buypage', views.buypage, name='buypage'),
]