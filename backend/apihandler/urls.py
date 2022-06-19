from django.urls import path
from . import views

urlpatterns = [
    path('', views.operation_two, name='operation_two'),
    path('PingTest', views.operation_one, name='operation_one'),
    path('LowFareSearch', views.operation_two, name='operation_two'),
    path('FareRule-<FlightNumber>', views.operation_three, name='operation_three'),
    path('Book&Ticket', views.operation_four, name='operation_four'),
]