from django.contrib import admin
from search_data.models import SearchData, BookedTicket, PassengerType, Tax, PassengerInfo


class SearchDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin', 'departureDateTime', 'returnDateTime', 'destination', 'cabin', 'adultNum',
                    'childNum', 'infantNum', 'returnStatus', 'creator_id')

    def save_model(self, request, obj, form, change):

        obj.creator_id = request.user
        super().save_model(request, obj, form, change)


class BookedTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'createdDateTime', 'flightNumber', 'departureDate', 'departureAirportLocationName',
                    'arrivalAirportLocationName', 'return_Status', 'return_DepartureDate', 'totalFareAmount', 'bookingReferenceID')


class PassengerTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'passengerTypeQuantity_Code', 'passengerTypeQuantity_Quantity')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'passengerType', 'taxName', 'tax_Amount')


class PassengerInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'personNameGivenName', 'personNameSurname', 'ticketingTicketDocumentNbr')


admin.site.register(SearchData, SearchDataAdmin)
admin.site.register(BookedTicket, BookedTicketAdmin)
admin.site.register(PassengerType, PassengerTypeAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(PassengerInfo, PassengerInfoAdmin)

