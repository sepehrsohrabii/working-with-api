from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buypage-<FlightNumber>', views.buypage, name='buypage'),
]