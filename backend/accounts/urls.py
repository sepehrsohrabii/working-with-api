from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='loginView'),
    path('signup/', views.signupView, name='signupView'),
    path('logout/', views.logoutView, name='logoutView'),
    path('profile/', views.userProfile, name='userProfile'),
    path('Ticket-<bookingReferenceID>', views.UserBookedTicketPage, name='UserBookedTicketPage'),
]