from django.contrib import admin
from search_data.models import SearchData, BookedTicket


class SearchDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin', 'departureDateTime', 'returnDateTime', 'destination', 'cabin', 'adultNum',
                    'childNum', 'infantNum', 'returnStatus', 'creator_id')

    def save_model(self, request, obj, form, change):

        obj.creator_id = request.user
        super().save_model(request, obj, form, change)

class BookedTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'traveler', 'ticketData')

    def save_model(self, request, obj, form, change):

        obj.traveler = request.user
        super().save_model(request, obj, form, change)


admin.site.register(SearchData, SearchDataAdmin)
admin.site.register(BookedTicket, BookedTicketAdmin)

