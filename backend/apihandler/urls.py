from django.urls import path
from . import views

urlpatterns = [
    path('', views.operation_one, name='operation_one'),
    path('LowFareSearch', views.operation_two, name='operation_two'),
    path('buypage-<FlightNumber>', views.buypage, name='buypage'),
]