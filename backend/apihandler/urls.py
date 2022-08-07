from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('Booking-<FlightNumber>', views.booking_page, name='booking_page'),
    path('read-reservation', views.read_reservation, name='read_reservation'),
    path('CancelingFee-<bookingReferenceID>', views.canceling_fee, name='canceling_fee'),
    #path('PingTest', views.operation_one, name='operation_one'),
    #path('LowFareSearch', views.operation_two, name='operation_two'),
    #path('FareRule-<FlightNumber>', views.operation_three, name='operation_three'),
    #path('Book&Ticket', views.operation_four, name='operation_four'),
]