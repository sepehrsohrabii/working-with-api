from django.contrib.auth.models import User
from django.db import models


class SearchData(models.Model):
    id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=20, null=True, blank=True)
    departureDateTime = models.DateTimeField(null=True, blank=True)
    returnDateTime = models.DateTimeField(null=True, blank=True)
    destination = models.CharField(max_length=20, null=True, blank=True)
    cabin = models.CharField(max_length=20, null=True, blank=True)
    adultNum = models.IntegerField(null=True, blank=True)
    childNum = models.IntegerField(null=True, blank=True)
    infantNum = models.IntegerField(null=True, blank=True)
    returnStatus = models.BooleanField(null=True, blank=True)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class BookedTicket(models.Model):
    STATUS = (
        ('Booked', 'Booked'),
        ('Canceled', 'Canceled'),
    )
    ticketStatus = models.CharField(max_length=50, choices=STATUS)
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    echoToken = models.CharField(max_length=10)
    createdDateTime = models.DateTimeField()
    directionInd = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    flightNumber = models.CharField(max_length=20)
    fareBasisCode = models.CharField(max_length=20)
    resBookDesigCode = models.CharField(max_length=20)
    departureDate = models.DateField()
    departureTime = models.TimeField()
    arrivalDate = models.DateField()
    arrivalTime = models.TimeField()
    stopQuantity = models.CharField(max_length=50, blank=True, null=True, default='0')
    RPH = models.CharField(max_length=20)
    departureAirportLocationCode = models.CharField(max_length=50)
    departureAirportLocationName = models.CharField(max_length=255)
    arrivalAirportLocationCode = models.CharField(max_length=50)
    arrivalAirportLocationName = models.CharField(max_length=255)
    operatingAirlineCode = models.CharField(max_length=30)
    equipmentAirEquipType = models.CharField(max_length=50)
    return_Status = models.CharField(max_length=10, blank=True, null=True)
    return_FlightNumber = models.CharField(max_length=10, blank=True, null=True)
    return_FareBasisCode = models.CharField(max_length=10, blank=True, null=True)
    return_ResBookDesigCode = models.CharField(max_length=10, blank=True, null=True)
    return_DepartureDate = models.DateField(blank=True, null=True)
    return_DepartureTime = models.TimeField(blank=True, null=True)
    return_ArrivalDate = models.DateField(blank=True, null=True)
    return_ArrivalTime = models.TimeField(blank=True, null=True)
    return_StopQuantity = models.CharField(max_length=50, blank=True, null=True)
    return_RPH = models.CharField(max_length=50, blank=True, null=True)
    return_DepartureAirportLocationCode = models.CharField(max_length=50, blank=True, null=True)
    return_DepartureAirportLocationName = models.CharField(max_length=50, blank=True, null=True)
    return_ArrivalAirportLocationCode = models.CharField(max_length=50, blank=True, null=True)
    return_ArrivalAirportLocationName = models.CharField(max_length=50, blank=True, null=True)
    return_OperatingAirlineCode = models.CharField(max_length=50, blank=True, null=True)
    return_EquipmentAirEquipType = models.CharField(max_length=50, blank=True, null=True)
    companyShortName = models.CharField(max_length=20)
    companyCode = models.CharField(max_length=50)
    totalFareCurrencyCode = models.CharField(max_length=50)
    totalFareDecimalPlaces = models.CharField(max_length=50)
    totalFareAmount = models.IntegerField()

    contactPersonGivenName = models.CharField(max_length=30)
    contactPersonSurname = models.CharField(max_length=30)
    contactPersonMobile = models.CharField(max_length=30)
    contactPersonHomeTelephone = models.CharField(max_length=30)
    contactPersonEmail = models.CharField(max_length=30)
    paymentType = models.CharField(max_length=30)
    directBill_ID = models.CharField(max_length=30)
    companyAgentType = models.CharField(max_length=30)
    paymentAmountCurrencyCode = models.CharField(max_length=30)
    paymentAmountDecimalPlaces = models.CharField(max_length=30)
    paymentAmountAmount = models.CharField(max_length=30)

    bookingReferenceIDStatus = models.CharField(max_length=30)
    bookingReferenceIDInstance = models.CharField(max_length=30)
    bookingReferenceID = models.CharField(max_length=30)
    bookingReferenceID_Context = models.CharField(max_length=30)

    fareRuleText = models.TextField(max_length=1000, blank=True, null=True)


class PassengerType(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(BookedTicket, on_delete=models.CASCADE, null=True, blank=True)
    passengerTypeQuantity_Code = models.CharField(max_length=10)
    passengerTypeQuantity_Quantity = models.IntegerField()
    fareBasisCode = models.CharField(max_length=10)
    passengerFare_BaseFare_CurrencyCode = models.CharField(max_length=5)
    passengerFare_BaseFare_DecimalPlaces = models.CharField(max_length=10)
    passengerFare_BaseFare_Amount = models.IntegerField()
    passengerFare_TotalFare_CurrencyCode = models.CharField(max_length=10)
    passengerFare_TotalFare_DecimalPlaces = models.CharField(max_length=10)
    passengerFare_TotalFare_Amount = models.IntegerField()
    fareInfo_FareInfo_FareBasisCode = models.CharField(max_length=10)
    fareInfo_FareInfo_BaseAmount = models.IntegerField()


class Tax(models.Model):
    id = models.AutoField(primary_key=True)
    passengerType = models.ForeignKey(PassengerType, on_delete=models.CASCADE, null=True, blank=True)
    taxText = models.CharField(max_length=50, blank=True, null=True)
    taxCode = models.CharField(max_length=10)
    taxName = models.CharField(max_length=50)
    tax_CurrencyCode = models.CharField(max_length=10)
    tax_DecimalPlaces = models.CharField(max_length=10)
    tax_Amount = models.IntegerField()


class PassengerInfo(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(BookedTicket, on_delete=models.CASCADE, null=True, blank=True)
    airTravelerBirthDate = models.CharField(max_length=10)
    airTravelerPassengerTypeCode = models.CharField(max_length=10)
    airTravelerABIInd = models.CharField(max_length=10)
    airTravelerTravelerNationality = models.CharField(max_length=10)
    airTravelerGender = models.CharField(max_length=5)
    personNameNamePrefix = models.CharField(max_length=10)
    personNameGivenName = models.CharField(max_length=50)
    personNameSurname = models.CharField(max_length=50)
    documentId = models.CharField(max_length=50)
    documentType = models.CharField(max_length=50)
    documentHolderNationality = models.CharField(max_length=5)
    travelerRefNumberRPH = models.CharField(max_length=50)

    ticketingTravelerRefNumber = models.CharField(max_length=50)
    ticketingTicketDocumentNbr = models.CharField(max_length=50)
