from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import requests
import re
from datetime import datetime
import xml.etree.ElementTree as ET
from copy import deepcopy
from search_data.models import BookedTicket, SearchData
#from guest_user.decorators import allow_guest_user
from django.contrib.auth.models import User

context = {}
flight_list = []
PTC_FBs = []
Taxes = []
passengers = []
operation_one_RS = []
selected_flight = []
Error = []
operation_three_RS = {}
Travelers_info = []
Ticketing_RefDocNUM = []
Ticket = {}


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#@allow_guest_user
def home_page(request):
    selected_operation_number = 2
    global origin
    global destination
    global departureTime
    global return_date
    global ADTNumber
    global CHDNumber
    global INFNumber
    global Cabin
    global user
    origin = request.POST.get("origin") or 'None'  # get flight origin from template input
    destination = request.POST.get("destination") or 'None'  # get flight destination from template input
    departureTime = request.POST.get(
        "departureTime") or datetime.now().isoformat()  # get flight departureTime from template input
    ADTNumber = request.POST.get("ADTNumber") or '1'  # get number of people from template input
    CHDNumber = request.POST.get("CHDNumber") or '0'  # get number of people from template input
    INFNumber = request.POST.get("INFNumber") or '0'  # get number of people from template input
    Cabin = request.POST.get("Cabin") or 'Economy'  # get number of people from template input
    return_date = request.POST.get("return_date") or 'None'

    # when user clicks on the submit button of form
    if request.method == 'POST':
        flight_list.clear()
        selected_flight.clear()
        if request.user.is_authenticated:
            user = request.user
        else:
            user = User.objects.get(username='Guest')
        data_handle(selected_operation_number)
    # send data to template
    operation_two_data = {
        'flight_list': flight_list,  # for results
        'ADTNumber': ADTNumber,  # for number of Adults which is in popup
        'CHDNumber': CHDNumber,  # for number of Children which is in popup
        'INFNumber': INFNumber,  # for number of Babies which is in popup
        'origin': origin,  # for nothing found result
        'destination': destination,  # for nothing found result
        'departureTime': departureTime,
    }
    return render(request, './home.html', operation_two_data)


@login_required(login_url='loginView')
def booking_page(request, FlightNumber):
    submit = request.POST.get('submit')
    if submit:
        passengers.clear()
        Error.clear()
        flight_list.clear()
        selected_operation_number = 4
        for passenger in selected_flight[0]['PTC_FBs']:
            for passenger_Quantity in range(1, int(passenger['PassengerTypeQuantity_Quantity']) + 1):
                NamePrefix_str = str(
                    "NamePrefix" + str(passenger_Quantity) + str(passenger['PassengerTypeQuantity_Code']))
                NamePrefix = request.POST.get(NamePrefix_str)
                GivenName_str = str(
                    "GivenName" + str(passenger_Quantity) + str(passenger['PassengerTypeQuantity_Code']))
                GivenName = request.POST.get(GivenName_str)
                SureName_str = str("SureName" + str(passenger_Quantity) + str(passenger['PassengerTypeQuantity_Code']))
                SureName = request.POST.get(SureName_str)
                BirthDate_str = str(
                    "BirthDate" + str(passenger_Quantity) + str(passenger['PassengerTypeQuantity_Code']))
                BirthDate = request.POST.get(BirthDate_str)
                Gender_str = str("Gender" + str(passenger_Quantity) + str(passenger['PassengerTypeQuantity_Code']))
                Gender = request.POST.get(Gender_str)
                TravelerNationality_str = str(
                    "TravelerNationality" + str(passenger_Quantity) + str(passenger['PassengerTypeQuantity_Code']))
                TravelerNationality = request.POST.get(TravelerNationality_str)
                DocID_str = str("DocID" + str(passenger_Quantity) + str(passenger['PassengerTypeQuantity_Code']))
                DocID = request.POST.get(DocID_str)
                passengers.append({
                    'NamePrefix': NamePrefix,
                    'GivenName': GivenName,
                    'SureName': SureName,
                    'BirthDate': BirthDate,
                    'Gender': Gender,
                    'TravelerNationality': TravelerNationality,
                    'DocID': DocID,
                    'TypeCode': str(passenger['PassengerTypeQuantity_Code']),
                })

        global ContactGivenName
        global ContactSureName
        global Email
        global Telephone
        global HomeTelephone
        ContactGivenName = request.POST.get('ContactGivenName')
        ContactSureName = request.POST.get('ContactSureName')
        Email = request.POST.get('Email')
        Telephone = request.POST.get('Telephone')
        HomeTelephone = request.POST.get('HomeTelephone')
        data_handle(selected_operation_number)
        user = request.user
        selected_operation_number = 5
        data_handle(selected_operation_number)
        return redirect('read_reservation')
    else:
        selected_operation_number = 3
        selected_flight.clear()
        for Flight in flight_list:
            if Flight['FlightNumber'] == FlightNumber:
                selected_flight.append(Flight)
                flight_list.clear()

        data_handle(selected_operation_number)

    return render(request, './booking.html',
                  {'selected_flight': selected_flight, 'Error': Error, 'operation_three_RS': operation_three_RS})


@login_required(login_url='loginView')
def read_reservation(request):
    
    return render(request, './read_reservation.html', Ticket)


def source_table():
    Operation = []
    Request_Schema = []
    Response_Schema = []
    Resource = []

    with open('/home/sepehr/Desktop/working-with-api/backend/apihandler/data/table source.txt') as file:
        for row in file:
            row = row.strip()
            op = row[:row.index(',')]
            Operation.append(op)
            RQ = re.findall(', (.*RQ.xsd)', row)

            Request_Schema.append(RQ[0])
            RS = re.findall('xsd (.*RS.xsd)', row)
            Response_Schema.append(RS[0])
            resource = re.findall('/.*', row)
            Resource.append(resource[0])
    return Operation, Request_Schema, Response_Schema, Resource


def write_on_xml(selected_operation_number):
    Agent_id = 'MOW07603'
    Operation, Request_Schema, Response_Schema, Resource = source_table()
    selected_operation = Operation[selected_operation_number - 1]
    # print('you select %s' % selected_operation)
    selected_Request_Schema = Request_Schema[selected_operation_number - 1]
    path = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}.xml'.format(
        selected_Request_Schema[:-4])
    newpath = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(
        selected_Request_Schema[:-4])
    tree = ET.parse(path)
    root = tree.getroot()
    root[0][0][0].attrib['ID'] = Agent_id
    root[0][0].attrib['ISOCurrency'] = "RUB"
    root.attrib['Target'] = 'Test'  # Test or Production
    root.attrib['TimeStamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    root.attrib['EchoToken'] = '0001'

    if selected_operation_number == 1:
        root[1].text = pingRQ

    elif selected_operation_number == 2:
        if return_date == 'None':
            root[1][0].text = departureTime
            root[1][1].attrib['LocationCode'] = origin
            root[1][2].attrib['LocationCode'] = destination
            root[2][0].attrib['Cabin'] = Cabin
            root[3][0][0].attrib['Quantity'] = ADTNumber
            root[3][0][1].attrib['Quantity'] = CHDNumber
            root[3][0][2].attrib['Quantity'] = INFNumber

        if return_date != 'None':
            date = root[1]
            returndate = deepcopy(date)
            root.insert(2, returndate)
            root[1][0].text = departureTime
            root[1][1].attrib['LocationCode'] = origin
            root[1][2].attrib['LocationCode'] = destination
            root[2][0].text = return_date
            root[2][1].attrib['LocationCode'] = destination
            root[2][2].attrib['LocationCode'] = origin
            root[3][0].attrib['Cabin'] = Cabin
            root[4][0][0].attrib['Quantity'] = ADTNumber
            root[4][0][1].attrib['Quantity'] = CHDNumber
            root[4][0][2].attrib['Quantity'] = INFNumber

    elif selected_operation_number == 3:
        root[1][0][0].attrib['FlightNumber'] = selected_flight[0]['FlightNumber']
        root[1][0][0].attrib['ResBookDesigCode'] = selected_flight[0]['ResBookDesigCode']
        root[1][0][0].attrib['DepartureDateTime'] = selected_flight[0]['departureDate'] + 'T' + \
                                                    selected_flight[0]['departureTime']
        root[1][0][0].attrib['ArrivalDateTime'] = selected_flight[0]['ArrivalDate'] + 'T' + selected_flight[0][
            'ArrivalTime']
        root[1][0][0].attrib['Duration'] = selected_flight[0]['Duration']
        root[1][0][0].attrib['StopQuantity'] = selected_flight[0]['StopQuantity']
        root[1][0][0].attrib['RPH'] = selected_flight[0]['RPH']
        root[1][0][0][0].attrib['LocationCode'] = selected_flight[0]['origin']
        root[1][0][0][1].attrib['LocationCode'] = selected_flight[0]['destination']
        root[1][0][0][2].attrib['Code'] = selected_flight[0]['OperatingAirline']
        root[1][0][0][3].attrib['AirEquipType'] = selected_flight[0]['AirEquipType']
        root[1][0][0][4][0].attrib['ResBookDesigCode'] = selected_flight[0]['ResBookDesigCode']
        root[1][0][0][4][0].attrib['ResBookDesigQuantity'] = selected_flight[0]['ResBookDesigQuantity']
        n = 0
        for PTC_FB in selected_flight[0]['PTC_FBs']:
            if n > 0:
                root[2].append(deepcopy(root[2][n - 1]))

            root[2][n].text = PTC_FB['FareBasisCode']
            root[2][n].attrib['FlightSegmentRPH'] = PTC_FB['FareBasisCode_FlightSegmentRPH']
            root[2][n].attrib['fareRPH'] = PTC_FB['FareBasisCode_fareRPH']
            n = n + 1

    elif selected_operation_number == 4:

        root[1].attrib['DirectionInd'] = "OneWay"
        root[1][0][0][0].attrib['FlightNumber'] = selected_flight[0]['FlightNumber']
        root[1][0][0][0].attrib['ResBookDesigCode'] = selected_flight[0]['ResBookDesigCode']
        root[1][0][0][0].attrib['DepartureDateTime'] = selected_flight[0]['departureDate'] + 'T' + \
                                                       selected_flight[0]['departureTime']
        root[1][0][0][0].attrib['ArrivalDateTime'] = selected_flight[0]['ArrivalDate'] + 'T' + \
                                                     selected_flight[0]['ArrivalTime']
        root[1][0][0][0].attrib['Duration'] = selected_flight[0]['Duration']
        root[1][0][0][0].attrib['StopQuantity'] = selected_flight[0]['StopQuantity']
        root[1][0][0][0].attrib['RPH'] = selected_flight[0]['RPH']
        root[1][0][0][0][0].attrib['LocationCode'] = selected_flight[0]['origin']
        root[1][0][0][0][1].attrib['LocationCode'] = selected_flight[0]['destination']
        root[1][0][0][0][2].attrib['Code'] = selected_flight[0]['OperatingAirline']
        root[1][0][0][0][3].attrib['AirEquipType'] = selected_flight[0]['AirEquipType']
        root[1][0][0][0][4][0].attrib['ResBookDesigCode'] = selected_flight[0]['ResBookDesigCode']
        root[1][0][0][0][4][0].attrib['ResBookDesigQuantity'] = selected_flight[0]['ResBookDesigQuantity']

        if 'return_date' in selected_flight[0]:
            root[1].attrib['DirectionInd'] = "Return"
            root[1][0].append(deepcopy(root[1][0][0]))
            root[1][0][1][0].attrib['FlightNumber'] = selected_flight[0]['Return_FlightNumber']
            root[1][0][1][0].attrib['ResBookDesigCode'] = selected_flight[0]['Return_ResBookDesigCode']
            root[1][0][1][0].attrib['DepartureDateTime'] = selected_flight[0]['Return_departureDate'] + 'T' + \
                                                           selected_flight[0]['Return_departureTime']
            root[1][0][1][0].attrib['ArrivalDateTime'] = selected_flight[0]['Return_ArrivalDate'] + 'T' + \
                                                         selected_flight[0]['Return_ArrivalTime']
            root[1][0][1][0].attrib['Duration'] = selected_flight[0]['Return_Duration']
            root[1][0][1][0].attrib['StopQuantity'] = selected_flight[0]['Return_StopQuantity']
            root[1][0][1][0].attrib['RPH'] = selected_flight[0]['Return_RPH']
            root[1][0][1][0][0].attrib['LocationCode'] = selected_flight[0]['Return_origin']
            root[1][0][1][0][1].attrib['LocationCode'] = selected_flight[0]['Return_destination']
            root[1][0][1][0][2].attrib['Code'] = selected_flight[0]['Return_OperatingAirline']
            root[1][0][1][0][3].attrib['AirEquipType'] = selected_flight[0]['Return_AirEquipType']
            root[1][0][1][0][4][0].attrib['ResBookDesigCode'] = selected_flight[0]['Return_ResBookDesigCode']
            root[1][0][1][0][4][0].attrib['ResBookDesigQuantity'] = selected_flight[0]['Return_ResBookDesigQuantity']

        root[2][0][0].attrib['CurrencyCode'] = selected_flight[0]['BaseFare_CurrencyCode']
        root[2][0][0].attrib['DecimalPlaces'] = selected_flight[0]['BaseFare_DecimalPlaces']
        root[2][0][0].attrib['Amount'] = selected_flight[0]['BaseFare_Amount']
        root[2][0][1].attrib['CurrencyCode'] = selected_flight[0]['TotalFare_CurrencyCode']
        root[2][0][1].attrib['DecimalPlaces'] = selected_flight[0]['TotalFare_DecimalPlaces']
        root[2][0][1].attrib['Amount'] = selected_flight[0]['TotalFare_Amount']

        i = 0
        for passenger in passengers:
            if i > 0:
                root[3].append(deepcopy(root[3][i - 1]))
            root[3][i].attrib['BirthDate'] = passenger['BirthDate']
            root[3][i].attrib['PassengerTypeCode'] = passenger['TypeCode']
            root[3][i].attrib['AccompaniedByInfantInd'] = "false"
            root[3][i].attrib['Gender'] = passenger['Gender']
            root[3][i].attrib['TravelerNationality'] = passenger['TravelerNationality']
            root[3][i][0][0].text = passenger['NamePrefix']
            root[3][i][0][1].text = passenger['GivenName']
            root[3][i][0][2].text = passenger['SureName']
            root[3][i][1].attrib['RPH'] = "1"
            root[3][i][2].attrib['DocID'] = passenger['DocID']
            root[3][i][2].attrib['DocType'] = "5"
            root[3][i][2].attrib['DocIssueCountry'] = "IR"
            root[3][i][2].attrib['ExpireDate'] = "2024-05-19"
            root[3][i][2].attrib['DocHolderNationality'] = "IR"
            i = i + 1

        root[4][0][0].text = ContactGivenName
        root[4][0][1].text = ContactSureName
        root[4][1].attrib['PhoneNumber'] = Telephone
        root[4][2].attrib['PhoneNumber'] = HomeTelephone
        root[4][3].text = Email
        root[5][0][0].attrib['PaymentType'] = "2"
        root[5][0][0][0].attrib['DirectBill_ID'] = Agent_id
        root[5][0][0][0][0].attrib['CompanyShortName'] = "PERSINO"
        root[5][0][0][0][0].attrib['Code'] = Agent_id
        root[5][0][0][1].attrib['CurrencyCode'] = selected_flight[0]['TotalFare_CurrencyCode']
        root[5][0][0][1].attrib['DecimalPlaces'] = selected_flight[0]['TotalFare_DecimalPlaces']
        root[5][0][0][1].attrib['Amount'] = selected_flight[0]['TotalFare_Amount']

    elif selected_operation_number == 5:

        root[1].attrib['ID'] = BookingReferenceID

    tree.write(newpath)
    with open(newpath) as file:
        xmlfile = file.read()
    return xmlfile


def read_from_xml(selected_operation_number, respath):
    Operation, Request_Schema, Response_Schema, Resource = source_table()
    tree = ET.parse(respath)
    root = tree.getroot()
    if selected_operation_number == 1:
        if 'Success' in root[1].tag:
            root_1_tag = 'Success'
        else:
            root_1_tag = ''
        operation_one_RS.append({
            'EchoData': root[0].text,
            'PingRS': root_1_tag
        })

    elif selected_operation_number == 2:
        if 'Success' in root[0].tag:
            for PricedItinerary in root[1]:
                SequenceNumber = PricedItinerary.attrib['SequenceNumber']
                FlightSegment = PricedItinerary[0][0][0][0]
                FlightNumber = FlightSegment.attrib['FlightNumber']
                ResBookDesigCode = FlightSegment.attrib['ResBookDesigCode']
                DepartureDateTime = FlightSegment.attrib['DepartureDateTime'].split('T')
                departureDate = DepartureDateTime[0]
                departureTime = DepartureDateTime[1].replace("+03", "+04")
                departureTime_model = departureTime.split(':')
                departureTime_model = departureTime_model[0] + ':' + departureTime_model[1]
                ArrivalDateTime = FlightSegment.attrib['ArrivalDateTime'].split('T')
                ArrivalDate = ArrivalDateTime[0]
                ArrivalTime = ArrivalDateTime[1]
                Duration = FlightSegment.attrib['Duration'].split(":")
                Duration[0] = int(Duration[0]) - 1
                Duration = '0' + str(Duration[0]) + ':' + Duration[1] + ':' + Duration[2]
                StopQuantity = FlightSegment.attrib['StopQuantity']
                RPH = FlightSegment.attrib['RPH']
                origin = FlightSegment[0].attrib['LocationCode']
                destination = FlightSegment[1].attrib['LocationCode']
                OperatingAirline = FlightSegment[2].attrib['Code']
                AirEquipType = FlightSegment[3].attrib['AirEquipType']
                ResBookDesigQuantity = FlightSegment[4][0].attrib['ResBookDesigQuantity']
                if return_date != 'None':
                    Return_FlightSegment = PricedItinerary[0][0][1][0]
                    Return_FlightNumber = Return_FlightSegment.attrib['FlightNumber']
                    Return_ResBookDesigCode = Return_FlightSegment.attrib['ResBookDesigCode']
                    Return_DepartureDateTime = Return_FlightSegment.attrib['DepartureDateTime'].split('T')
                    Return_departureDate = Return_DepartureDateTime[0]
                    Return_departureTime = Return_DepartureDateTime[1].replace("+03", "+04")
                    Return_departureTime_model = Return_departureTime.split(':')
                    Return_departureTime_model = Return_departureTime_model[0] + ':' + Return_departureTime_model[1]
                    Return_ArrivalDateTime = Return_FlightSegment.attrib['ArrivalDateTime'].split('T')
                    Return_ArrivalDate = Return_ArrivalDateTime[0]
                    Return_ArrivalTime = Return_ArrivalDateTime[1]
                    Return_Duration = Return_FlightSegment.attrib['Duration'].split(":")
                    Return_Duration[0] = int(Return_Duration[0]) - 1
                    Return_Duration = '0' + str(Return_Duration[0]) + ':' + Return_Duration[1] + ':' + Return_Duration[
                        2]
                    Return_StopQuantity = Return_FlightSegment.attrib['StopQuantity']
                    Return_RPH = Return_FlightSegment.attrib['RPH']
                    Return_origin = Return_FlightSegment[0].attrib['LocationCode']
                    Return_destination = Return_FlightSegment[1].attrib['LocationCode']
                    Return_OperatingAirline = Return_FlightSegment[2].attrib['Code']
                    Return_AirEquipType = Return_FlightSegment[3].attrib['AirEquipType']
                    Return_ResBookDesigQuantity = Return_FlightSegment[4][0].attrib['ResBookDesigQuantity']

                BaseFare_CurrencyCode = PricedItinerary[1][0][0].attrib['CurrencyCode']
                BaseFare_DecimalPlaces = PricedItinerary[1][0][0].attrib['DecimalPlaces']
                BaseFare_Amount = PricedItinerary[1][0][0].attrib['Amount']
                TotalFare_CurrencyCode = PricedItinerary[1][0][1].attrib['CurrencyCode']
                TotalFare_DecimalPlaces = PricedItinerary[1][0][1].attrib['DecimalPlaces']
                TotalFare_Amount = PricedItinerary[1][0][1].attrib['Amount']
                PTC_FareBreakdowns = PricedItinerary[1][1]
                PTC_FBs.clear()
                for PTC_FareBreakdown in PTC_FareBreakdowns:
                    PassengerTypeQuantity_Code = PTC_FareBreakdown[0].attrib['Code']
                    PassengerTypeQuantity_Quantity = PTC_FareBreakdown[0].attrib['Quantity']
                    FareBasisCode = PTC_FareBreakdown[1][0].text
                    FareBasisCode_FlightSegmentRPH = PTC_FareBreakdown[1][0].attrib['FlightSegmentRPH']
                    FareBasisCode_fareRPH = PTC_FareBreakdown[1][0].attrib['fareRPH']
                    PassengerFare_BaseFare_CurrencyCode = PTC_FareBreakdown[2][0].attrib['CurrencyCode']
                    PassengerFare_BaseFare_DecimalPlaces = PTC_FareBreakdown[2][0].attrib['DecimalPlaces']
                    PassengerFare_BaseFare_Amount = PTC_FareBreakdown[2][0].attrib['Amount']
                    PassengerFare_Taxes = PTC_FareBreakdown[2][1]
                    Taxes.clear()
                    for Tax in PassengerFare_Taxes:
                        TaxText = Tax.text
                        TaxCode = Tax.attrib['TaxCode']
                        TaxName = Tax.attrib['TaxName']
                        Tax_CurrencyCode = Tax.attrib['CurrencyCode']
                        Tax_DecimalPlaces = Tax.attrib['DecimalPlaces']
                        Taxes.append({
                            'TaxText': TaxText,
                            'TaxCode': TaxCode,
                            'TaxName': TaxName,
                            'Tax_CurrencyCode': Tax_CurrencyCode,
                            'Tax_DecimalPlaces': Tax_DecimalPlaces,
                        })
                    PTC_FBs.append({
                        'PassengerTypeQuantity_Code': PassengerTypeQuantity_Code,
                        'PassengerTypeQuantity_Quantity': PassengerTypeQuantity_Quantity,
                        'PassengerTypeQuantity_Range': range(1, int(PassengerTypeQuantity_Quantity) + 1),
                        'FareBasisCode': FareBasisCode,
                        'FareBasisCode_FlightSegmentRPH': FareBasisCode_FlightSegmentRPH,
                        'FareBasisCode_fareRPH': FareBasisCode_fareRPH,
                        'PassengerFare_BaseFare_CurrencyCode': PassengerFare_BaseFare_CurrencyCode,
                        'PassengerFare_BaseFare_DecimalPlaces': PassengerFare_BaseFare_DecimalPlaces,
                        'PassengerFare_BaseFare_Amount': PassengerFare_BaseFare_Amount,
                        'Taxes': Taxes,
                    })
                if return_date == 'None':
                    flight_list.append({
                        'SequenceNumber': SequenceNumber,
                        'FlightNumber': FlightNumber,
                        'ResBookDesigCode': ResBookDesigCode,
                        'departureDate': departureDate,
                        'departureTime': departureTime,
                        'ArrivalDate': ArrivalDate,
                        'ArrivalTime': ArrivalTime,
                        'Duration': Duration,
                        'StopQuantity': StopQuantity,
                        'RPH': RPH,
                        'origin': origin,
                        'destination': destination,
                        'OperatingAirline': OperatingAirline,
                        'AirEquipType': AirEquipType,
                        'ResBookDesigQuantity': ResBookDesigQuantity,
                        'BaseFare_CurrencyCode': BaseFare_CurrencyCode,
                        'BaseFare_DecimalPlaces': BaseFare_DecimalPlaces,
                        'BaseFare_Amount': BaseFare_Amount,
                        'TotalFare_CurrencyCode': TotalFare_CurrencyCode,
                        'TotalFare_DecimalPlaces': TotalFare_DecimalPlaces,
                        'TotalFare_Amount': TotalFare_Amount,
                        'PTC_FBs': PTC_FBs,
                    })
                if return_date != 'None':
                    flight_list.append({
                        'SequenceNumber': SequenceNumber,
                        'FlightNumber': FlightNumber,
                        'ResBookDesigCode': ResBookDesigCode,
                        'departureDate': departureDate,
                        'departureTime': departureTime,
                        'ArrivalDate': ArrivalDate,
                        'ArrivalTime': ArrivalTime,
                        'Duration': Duration,
                        'StopQuantity': StopQuantity,
                        'RPH': RPH,
                        'origin': origin,
                        'destination': destination,
                        'OperatingAirline': OperatingAirline,
                        'AirEquipType': AirEquipType,
                        'ResBookDesigQuantity': ResBookDesigQuantity,
                        'BaseFare_CurrencyCode': BaseFare_CurrencyCode,
                        'BaseFare_DecimalPlaces': BaseFare_DecimalPlaces,
                        'BaseFare_Amount': BaseFare_Amount,
                        'TotalFare_CurrencyCode': TotalFare_CurrencyCode,
                        'TotalFare_DecimalPlaces': TotalFare_DecimalPlaces,
                        'TotalFare_Amount': TotalFare_Amount,
                        'PTC_FBs': PTC_FBs,
                        'return_date': return_date,
                        'Return_FlightNumber': Return_FlightNumber,
                        'Return_ResBookDesigCode': Return_ResBookDesigCode,
                        'Return_departureDate': Return_departureDate,
                        'Return_departureTime': Return_departureTime,
                        'Return_ArrivalDate': Return_ArrivalDate,
                        'Return_ArrivalTime': Return_ArrivalTime,
                        'Return_Duration': Return_Duration,
                        'Return_StopQuantity': Return_StopQuantity,
                        'Return_RPH': Return_RPH,
                        'Return_origin': Return_origin,
                        'Return_destination': Return_destination,
                        'Return_OperatingAirline': Return_OperatingAirline,
                        'Return_AirEquipType': Return_AirEquipType,
                        'Return_ResBookDesigQuantity': Return_ResBookDesigQuantity,
                    })
            search_data = SearchData()
            search_data.origin = origin
            search_data.departureDateTime = departureDate + ' ' + departureTime_model
            search_data.returnStatus = False
            if return_date != 'None':
                search_data.returnDateTime = Return_departureDate + ' ' + Return_departureTime_model
                search_data.returnStatus = True
            search_data.destination = destination
            search_data.cabin = Cabin
            search_data.adultNum = ADTNumber
            search_data.childNum = CHDNumber
            search_data.infantNum = INFNumber
            if user.is_authenticated:
                search_data.creator_id = user
            else:
                search_data.creator_id = User.objects.get(username='Guest')
            search_data.save()

    elif selected_operation_number == 3:
        if 'Success' in root[0].tag:
            try:
                FareRuleText = root[2][0].text
                FlightRefNumberRPH = root[2][1].text
            except:
                FareRuleText = ''
                FlightRefNumberRPH = ''

            operation_three_RS = {
                'Status': 'Success',
                'FlightNumber': root[1][0][0].attrib['FlightNumber'],
                'ResBookDesigCode': root[1][0][0].attrib['ResBookDesigCode'],
                'DepartureDateTime': root[1][0][0].attrib['DepartureDateTime'],
                'ArrivalDateTime': root[1][0][0].attrib['ArrivalDateTime'],
                'Duration': root[1][0][0].attrib['Duration'],
                'StopQuantity': root[1][0][0].attrib['StopQuantity'],
                'RPH': root[1][0][0].attrib['RPH'],
                'DepartureAirport': root[1][0][0][0].attrib['LocationCode'],
                'ArrivalAirport': root[1][0][0][1].attrib['LocationCode'],
                'OperatingAirline': root[1][0][0][2].attrib['Code'],
                'AirEquipType': root[1][0][0][3].attrib['AirEquipType'],
                'ResBookDesigCode': root[1][0][0][4][0].attrib['ResBookDesigCode'],
                'ResBookDesigQuantity': root[1][0][0][4][0].attrib['ResBookDesigQuantity'],
                'FareRuleText': FareRuleText,
                'FlightRefNumberRPH': FlightRefNumberRPH
            }

    elif selected_operation_number == 4:
        if 'Success' in root[0].tag:
            i = 6
            Travelers = root[1][3]
            for Traveler in Travelers:
                i = i + 1

            global BookingReferenceID
            BookingReferenceID = root[1][i].attrib['ID']
        else:
            ErrorText = root[0][0].attrib['ShortText'] or 'None'
            ErrorCode = root[0][0].attrib['Code'] or 'None'
            Error.append({
                'ErrorText': ErrorText,
                'ErrorCode': ErrorCode
            })

    elif selected_operation_number == 5:
        if 'Success' in root[0].tag:
            CreatedDateTme = root[1].attrib['CreatedDateTme']
            DirectionInd = root[1][0].attrib['DirectionInd']
        
            FlightSegment = root[1][0][0][0][0]
            Status = FlightSegment.attrib['Status']
            FlightNumber = FlightSegment.attrib['FlightNumber']
            FareBasisCode = FlightSegment.attrib['FareBasisCode']
            ResBookDesigCode = FlightSegment.attrib['ResBookDesigCode']
            DepartureDateTime = FlightSegment.attrib['DepartureDateTime']
            ArrivalDateTime = FlightSegment.attrib['ArrivalDateTime']
            StopQuantity = FlightSegment.attrib['StopQuantity']
            RPH = FlightSegment.attrib['RPH']
            DepartureAirportLocationCode = FlightSegment[0].attrib['LocationCode']
            DepartureAirportLocationName = FlightSegment[0].attrib['LocationName']
            ArrivalAirportLocationCode = FlightSegment[1].attrib['LocationCode']
            ArrivalAirportLocationName = FlightSegment[1].attrib['LocationName']
            OperatingAirlineCode = FlightSegment[2].attrib['Code']
            EquipmentAirEquipType = FlightSegment[3].attrib['AirEquipType']
            
            Return_FlightSegment = 'None'
            Return_Status = 'None'
            Return_FlightNumber = 'None'
            Return_FareBasisCode = 'None'
            Return_ResBookDesigCode = 'None'
            Return_DepartureDateTime = 'None'
            Return_ArrivalDateTime = 'None'
            Return_StopQuantity = 'None'
            Return_RPH = 'None'
            Return_DepartureAirportLocationCode = 'None'
            Return_DepartureAirportLocationName = 'None'
            Return_ArrivalAirportLocationCode = 'None'
            Return_ArrivalAirportLocationName = 'None'
            Return_OperatingAirlineCode = 'None'
            Return_EquipmentAirEquipType = 'None'
            
            if DirectionInd == 'Return':
                Return_FlightSegment = root[1][0][0][0][1]
                Return_Status = FlightSegment.attrib['Status']
                Return_FlightNumber = FlightSegment.attrib['FlightNumber']
                Return_FareBasisCode = FlightSegment.attrib['FareBasisCode']
                Return_ResBookDesigCode = FlightSegment.attrib['ResBookDesigCode']
                Return_DepartureDateTime = FlightSegment.attrib['DepartureDateTime']
                Return_ArrivalDateTime = FlightSegment.attrib['ArrivalDateTime']
                Return_StopQuantity = FlightSegment.attrib['StopQuantity']
                Return_RPH = FlightSegment.attrib['RPH']
                Return_DepartureAirportLocationCode = FlightSegment[0].attrib['LocationCode']
                Return_DepartureAirportLocationName = FlightSegment[0].attrib['LocationName']
                Return_ArrivalAirportLocationCode = FlightSegment[1].attrib['LocationCode']
                Return_ArrivalAirportLocationName = FlightSegment[1].attrib['LocationName']
                Return_OperatingAirlineCode = FlightSegment[2].attrib['Code']
                Return_EquipmentAirEquipType = FlightSegment[3].attrib['AirEquipType']
            
            CompanyShortName = root[1][1][0].attrib['CompanyShortName']
            CompanyCode = root[1][1][0].attrib['Code']

            TotalFareCurrencyCode = root[1][2][0][0].attrib['CurrencyCode']
            TotalFareDecimalPlaces = root[1][2][0][0].attrib['DecimalPlaces']
            TotalFareAmount = root[1][2][0][0].attrib['Amount']
            PTC_FBs.clear()
            PTC_FareBreakdowns = root[1][2][1]
            for PTC_FareBreakdown in PTC_FareBreakdowns:
                PassengerTypeQuantity_Code = PTC_FareBreakdown[0].attrib['Code']
                PassengerTypeQuantity_Quantity = PTC_FareBreakdown[0].attrib['Quantity']
                FareBasisCode = PTC_FareBreakdown[1][0].text
                PassengerFare_BaseFare_CurrencyCode = PTC_FareBreakdown[2][0].attrib['CurrencyCode']
                PassengerFare_BaseFare_DecimalPlaces = PTC_FareBreakdown[2][0].attrib['DecimalPlaces']
                PassengerFare_BaseFare_Amount = PTC_FareBreakdown[2][0].attrib['Amount']
                PassengerFare_Taxes = PTC_FareBreakdown[2][1]
                Taxes.clear()
                for Tax in PassengerFare_Taxes:
                    TaxText = Tax.text or 'none'
                    TaxCode = Tax.attrib['TaxCode']
                    TaxName = Tax.attrib['TaxName']
                    Tax_CurrencyCode = Tax.attrib['CurrencyCode']
                    Tax_DecimalPlaces = Tax.attrib['DecimalPlaces']
                    Taxes.append({
                        'TaxText': TaxText,
                        'TaxCode': TaxCode,
                        'TaxName': TaxName,
                        'Tax_CurrencyCode': Tax_CurrencyCode,
                        'Tax_DecimalPlaces': Tax_DecimalPlaces,
                    })
                PassengerFare_TotalFare_CurrencyCode = PTC_FareBreakdown[2][2].attrib['CurrencyCode']
                PassengerFare_TotalFare_DecimalPlaces = PTC_FareBreakdown[2][2].attrib['DecimalPlaces']
                PassengerFare_TotalFare_Amount = PTC_FareBreakdown[2][2].attrib['Amount']

                FareInfo_FareInfo_FareBasisCode = PTC_FareBreakdown[3][0].attrib['FareBasisCode']
                FareInfo_FareInfo_BaseAmount = PTC_FareBreakdown[3][0][0].attrib['BaseAmount']

                PTC_FBs.append({
                    'PassengerTypeQuantity_Code': PassengerTypeQuantity_Code,
                    'PassengerTypeQuantity_Quantity': PassengerTypeQuantity_Quantity,
                    'FareBasisCode': FareBasisCode,
                    'PassengerFare_BaseFare_CurrencyCode': PassengerFare_BaseFare_CurrencyCode,
                    'PassengerFare_BaseFare_DecimalPlaces': PassengerFare_BaseFare_DecimalPlaces,
                    'PassengerFare_BaseFare_Amount': PassengerFare_BaseFare_Amount,
                    'Taxes': Taxes,
                    'PassengerFare_TotalFare_CurrencyCode': PassengerFare_TotalFare_CurrencyCode,
                    'PassengerFare_TotalFare_DecimalPlaces': PassengerFare_TotalFare_DecimalPlaces,
                    'PassengerFare_TotalFare_Amount': PassengerFare_TotalFare_Amount,
                    'FareInfo_FareInfo_FareBasisCode': FareInfo_FareInfo_FareBasisCode,
                    'FareInfo_FareInfo_BaseAmount': FareInfo_FareInfo_BaseAmount,
                })
            Travelers_info.clear()
            Travelers = root[1][3]
            for Traveler in Travelers:
                AirTravelerBirthDate = Traveler.attrib['BirthDate']
                AirTravelerPassengerTypeCode = Traveler.attrib['PassengerTypeCode']
                AirTravelerAccompaniedByInfantInd = Traveler.attrib['AccompaniedByInfantInd']
                AirTravelerTravelerNationality = Traveler.attrib['TravelerNationality']
                AirTravelerGender = Traveler.attrib['Gender']
                PersonNamePrefix = Traveler[0][0].text
                PersonNameGivenName = Traveler[0][1].text
                PersonNameSurname = Traveler[0][2].text
                DocumentId = Traveler[1].attrib['DocID']
                DocumentType = Traveler[1].attrib['DocType']
                DocumentHolderNationality = Traveler[1].attrib['DocHolderNationality']
                TravelerRefNumberRPH = Traveler[2].attrib['RPH']
                Travelers_info.append({
                    'AirTravelerBirthDate': AirTravelerBirthDate,
                    'AirTravelerPassengerTypeCode': AirTravelerPassengerTypeCode,
                    'AirTravelerAccompaniedByInfantInd': AirTravelerAccompaniedByInfantInd,
                    'AirTravelerTravelerNationality': AirTravelerTravelerNationality,
                    'AirTravelerGender': AirTravelerGender,
                    'PersonNameNamePrefix': PersonNamePrefix,
                    'PersonNameGivenName': PersonNameGivenName,
                    'PersonNameSurname': PersonNameSurname,
                    'DocumentId': DocumentId,
                    'DocumentType': DocumentType,
                    'DocumentHolderNationality': DocumentHolderNationality,
                    'TravelerRefNumberRPH': TravelerRefNumberRPH,
                })

            ContactPersonGivenName = root[1][4][0][0].text
            ContactPersonSurname = root[1][4][0][1].text
            ContactPersonMobile = root[1][4][1].attrib['PhoneNumber']
            ContactPersonHomeTelephone = root[1][4][2].attrib['PhoneNumber']
            ContactPersonEmail = root[1][4][3].text

            PaymentType = root[1][5][0][0].attrib['PaymentType']
            DirectBill_ID = root[1][5][0][0][0].attrib['DirectBill_ID']
            CompanyShortName = root[1][5][0][0][0][0].attrib['CompanyShortName']
            CompanyCode = root[1][5][0][0][0][0].attrib['Code']
            CompanyAgentType = root[1][5][0][0][0][0].attrib['AgentType']

            PaymentAmountCurrencyCode = root[1][5][0][0][1].attrib['CurrencyCode']
            PaymentAmountDecimalPlaces = root[1][5][0][0][1].attrib['DecimalPlaces']
            PaymentAmountAmount = root[1][5][0][0][1].attrib['Amount']

            i = 6
            Ticketing_RefDocNUM.clear()
            for Traveler in Travelers:
                Ticketing = root[1][i]
                TicketingTravelerRefNumber = Ticketing.attrib['TravelerRefNumber']
                TicketingTicketDocumentNbr = Ticketing.attrib['TicketDocumentNbr']
                i = i + 1
                Ticketing_RefDocNUM.append({
                    'TicketingTravelerRefNumber': TicketingTravelerRefNumber,
                    'TicketingTicketDocumentNbr': TicketingTicketDocumentNbr,
                })


            BookingReferenceIDStatus = root[1][i].attrib['Status']    
            BookingReferenceIDInstance = root[1][i].attrib['Instance']
            BookingReferenceID = root[1][i].attrib['ID']
            BookingReferenceID_Context = root[1][i].attrib['ID_Context']
            
            Ticket = {
                'CreatedDateTme': CreatedDateTme,
                'DirectionInd': DirectionInd,
                'Status': Status,
                'FlightNumber': FlightNumber,
                'FareBasisCode': FareBasisCode,
                'ResBookDesigCode': ResBookDesigCode,
                'DepartureDateTime': DepartureDateTime,
                'ArrivalDateTime': ArrivalDateTime,
                'RPH': RPH,
                'DepartureAirportLocationCode': DepartureAirportLocationCode,
                'DepartureAirportLocationName': DepartureAirportLocationName,
                'ArrivalAirportLocationCode': ArrivalAirportLocationCode,
                'ArrivalAirportLocationName': ArrivalAirportLocationName,
                'OperatingAirlineCode': OperatingAirlineCode,
                'EquipmentAirEquipType': EquipmentAirEquipType,
                'Return_Status': Return_Status or 'None',
                'Return_FlightNumber': Return_FlightNumber or 'None',
                'Return_FareBasisCode': Return_FareBasisCode or 'None',
                'Return_ResBookDesigCode': Return_ResBookDesigCode or 'None',
                'Return_DepartureDateTime': Return_DepartureDateTime or 'None',
                'Return_ArrivalDateTime': Return_ArrivalDateTime or 'None',
                'Return_StopQuantity': Return_StopQuantity or 'None',
                'Return_RPH': Return_RPH or 'None',
                'Return_DepartureAirportLocationCode': Return_DepartureAirportLocationCode or 'None',
                'Return_DepartureAirportLocationName': Return_DepartureAirportLocationName or 'None',
                'Return_ArrivalAirportLocationCode': Return_ArrivalAirportLocationCode or 'None',
                'Return_ArrivalAirportLocationName': Return_ArrivalAirportLocationName or 'None',
                'Return_OperatingAirlineCode': Return_OperatingAirlineCode or 'None',
                'Return_EquipmentAirEquipType': Return_EquipmentAirEquipType or 'None',
                'CompanyShortName': CompanyShortName,
                'CompanyCode': CompanyCode,
                'TotalFareCurrencyCode': TotalFareCurrencyCode,
                'TotalFareDecimalPlaces': TotalFareDecimalPlaces,
                'TotalFareAmount': TotalFareAmount,
                'PTC_FBs': PTC_FBs,
                'Travelers_info': Travelers_info,
                'ContactPersonGivenName': ContactPersonGivenName,
                'ContactPersonSurname': ContactPersonSurname,
                'ContactPersonMobile': ContactPersonMobile,
                'ContactPersonHomeTelephone': ContactPersonHomeTelephone,
                'ContactPersonEmail': ContactPersonEmail,
                'PaymentType': PaymentType,
                'DirectBill_ID': DirectBill_ID,
                'CompanyAgentType': CompanyAgentType,
                'PaymentAmountCurrencyCode': PaymentAmountCurrencyCode,
                'PaymentAmountDecimalPlaces': PaymentAmountDecimalPlaces,
                'PaymentAmountAmount': PaymentAmountAmount,
                'Ticketing_RefDocNUM': Ticketing_RefDocNUM,
                'BookingReferenceIDStatus': BookingReferenceIDStatus,
                'BookingReferenceIDInstance': BookingReferenceIDInstance,
                'BookingReferenceID': BookingReferenceID,
                'BookingReferenceID_Context': BookingReferenceID_Context,
            }
            bookedTicket = BookedTicket()
            bookedTicket.traveler = user
            bookedTicket.ticketData = str(Ticket)
            bookedTicket.save()

def data_handle(selected_operation_number):
    Agent_id = 'MOW07603'
    Operation, Request_Schema, Response_Schema, Resource = source_table()

    selected_Response_Schema = Response_Schema[selected_operation_number - 1]
    selected_Resource = Resource[selected_operation_number - 1]

    headers = {'Accept': 'application/xml',
               'Content-Type': 'application/xml',
               'Authorization': 'y00Lm/iuKNN6X8xU/p5FyJYVjXBCOh/JEQdcwPyGtJg='}
    endpoint = 'https://staging.homares.ir/wsbe/rest'
    url = endpoint + selected_Resource
    xmlfile = write_on_xml(selected_operation_number)
    response = requests.post(url=url, data=xmlfile, headers=headers)
    respath = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(
        selected_Response_Schema[:-4])
    with open(respath, 'w') as f:
        f.write(response.text)
    f.close()
    read_from_xml(selected_operation_number, respath)
