from apihandler.views import split_booking
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render
from search_data.models import SearchData, BookedTicket, PassengerInfo


@staff_member_required(redirect_field_name='next', login_url='/accounts/login')
def AdminPanel(request):
    searched_data = SearchData.objects.all()
    total_ticket_number = BookedTicket.objects.count()
    total_passenger_number = PassengerInfo.objects.count()
    tickets = BookedTicket.objects.all()
    total_ticket_price = 0
    for ticket in tickets:
        total_ticket_price += int(ticket.paymentAmountAmount)

    total_search_number = SearchData.objects.count()
    q = request.POST.get('search_input')
    if q:
        user_tickets = BookedTicket.objects.filter(
            Q(bookingReferenceID__icontains=q) | Q(user__username__icontains=q)).order_by('-createdDateTime')
    else:
        user_tickets = BookedTicket.objects.all().order_by('-createdDateTime')

    ticket_passengers = PassengerInfo.objects.all()
    if request.method == 'POST' and request.POST.get('split_bookingReferenceID'):
        split_booking(request)
    context = {
        'searched_data': searched_data,
        'user_tickets': user_tickets,
        'ticket_passengers': ticket_passengers,
        'total_ticket_number': total_ticket_number,
        'total_search_number': total_search_number,
        'total_ticket_price': total_ticket_price,
        'total_passenger_number': total_passenger_number,
    }
    return render(request, './panel.html', context)
