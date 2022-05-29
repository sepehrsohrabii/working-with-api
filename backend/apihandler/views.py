from django.shortcuts import render
import requests
from pathlib import Path
import re
from datetime import datetime
import xml.etree.ElementTree as ET
from copy import deepcopy

context = {}
flight_list = []
PTC_FBs = []
Taxes = []
passengers = []
operation_one_RS = []


def operation_one(request):
    global pingRQ
    pingRQ = request.POST.get("pingRQ") or ""
    selected_operation_number = 1
    operation_one_RS.clear()
    data_handle(selected_operation_number)
    operation_one_data = {
        'operation_one': selected_operation_number,
        'operation_one_RS': operation_one_RS[0]
    }
    return render(request, './operation_one.html', operation_one_data)


def operation_two(request):
    # data = json_load  # load JSON
    selected_operation_number = 2
    global origin
    global destination
    global departureTime
    global ADTNumber
    global CHDNumber
    global INFNumber
    global Cabin
    origin = request.POST.get("origin") or 'None'  # get flight origin from template input
    destination = request.POST.get("destination") or 'None'  # get flight destination from template input
    departureTime = request.POST.get(
        "departureTime") or datetime.now().isoformat()  # get flight departureTime from template input
    ADTNumber = request.POST.get("ADTNumber") or '0'  # get number of people from template input
    CHDNumber = request.POST.get("CHDNumber") or '0'  # get number of people from template input
    INFNumber = request.POST.get("INFNumber") or '0'  # get number of people from template input
    Cabin = request.POST.get("Cabin") or 'Economy'  # get number of people from template input
    data_list = []
    # when user clicks on the submit button of form
    if request.method == 'POST':
        data_list = []
        data_handle(selected_operation_number)
        for data1 in flight_list:  # turn in JSON data
            data_list.append({
                'origin': data1['origin'],
                'destination': data1['destination'],
                'departureDate': data1['departureDate'],
                'departureTime': data1['departureTime'],
                'ArrivalDate': data1['ArrivalDate'],
                'ArrivalTime': data1['ArrivalTime'],
                'Duration': data1['Duration'],
                'FlightNumber': data1['FlightNumber'],
                'AirEquipType': data1['AirEquipType'],
                'TotalFare_Amount': data1['TotalFare_Amount'],
                'TotalFare_CurrencyCode': data1['TotalFare_CurrencyCode'],
                'PTC_FBs': data1['PTC_FBs']
            })  # add result to results
        flight_list.clear()

    # send data to template
    operation_two_data = {
        'data_list': data_list,  # for results
        'ADTNumber': ADTNumber,  # for number of Adults which is in popup
        'CHDNumber': CHDNumber,  # for number of Children which is in popup
        'INFNumber': INFNumber,  # for number of Babies which is in popup
        'origin': origin,  # for nothing found result
        'destination': destination,  # for nothing found result
        'departureTime': departureTime,
    }
    return render(request, './operation_two.html', operation_two_data)


def operation_three(request, FlightNumber):
    Operation, Request_Schema, Response_Schema, Resource = source_table()
    global flight_list_booking
    flight_list_booking = []
    selected_operation_number = 2
    selected_Response_Schema = Response_Schema[selected_operation_number - 1]
    respath = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(
        selected_Response_Schema[:-4])
    tree = ET.parse(respath)
    root = tree.getroot()
    flight_list_booking.clear()
    for PricedItinerary in root[1]:
        FlightSegment = PricedItinerary[0][0][0][0]
        FlightNumberSRS = FlightSegment.attrib['FlightNumber']
        if FlightNumberSRS in FlightNumber:
            SequenceNumber = PricedItinerary.attrib['SequenceNumber']
            ResBookDesigCode = FlightSegment.attrib['ResBookDesigCode']
            DepartureDateTime = FlightSegment.attrib['DepartureDateTime'].split('T')
            departureDate = DepartureDateTime[0]
            departureTime = DepartureDateTime[1].replace("+04", "+03")
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

            flight_list_booking.append({
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
    selected_operation_number = 3
    data_handle(selected_operation_number)
    return render(request, './operation_three.html', operation_three_RS)


def operation_four(request, FlightNumber):
    Operation, Request_Schema, Response_Schema, Resource = source_table()
    global flight_list_booking
    flight_list_booking = []
    selected_operation_number = 2
    selected_Response_Schema = Response_Schema[selected_operation_number - 1]
    respath = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(
        selected_Response_Schema[:-4])
    tree = ET.parse(respath)
    root = tree.getroot()
    flight_list_booking.clear()
    for PricedItinerary in root[1]:
        FlightSegment = PricedItinerary[0][0][0][0]
        FlightNumberSRS = FlightSegment.attrib['FlightNumber']
        if FlightNumberSRS in FlightNumber:
            SequenceNumber = PricedItinerary.attrib['SequenceNumber']
            ResBookDesigCode = FlightSegment.attrib['ResBookDesigCode']
            DepartureDateTime = FlightSegment.attrib['DepartureDateTime'].split('T')
            departureDate = DepartureDateTime[0]
            departureTime = DepartureDateTime[1].replace("+04", "+03")
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

            flight_list_booking.append({
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

    submit = request.POST.get('submit')
    if submit:
        selected_operation_number = 4
        for passenger in flight_list_booking[0]['PTC_FBs']:
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

    operation_four_data = {
        'flight_list_booking': flight_list_booking,
    }
    return render(request, './operation_four.html', operation_four_data)


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
        root[1][0].text = departureTime
        root[1][1].attrib['LocationCode'] = origin
        root[1][2].attrib['LocationCode'] = destination
        root[3][0][0].attrib['Quantity'] = ADTNumber
        root[3][0][1].attrib['Quantity'] = CHDNumber
        root[3][0][2].attrib['Quantity'] = INFNumber
        root[2][0].attrib['Cabin'] = Cabin

    elif selected_operation_number == 3:
        root[1][0][0].attrib['FlightNumber'] = flight_list_booking[0]['FlightNumber']
        root[1][0][0].attrib['ResBookDesigCode'] = flight_list_booking[0]['ResBookDesigCode']
        root[1][0][0].attrib['DepartureDateTime'] = flight_list_booking[0]['departureDate'] + 'T' + \
                                                    flight_list_booking[0]['departureTime']
        root[1][0][0].attrib['ArrivalDateTime'] = flight_list_booking[0]['ArrivalDate'] + 'T' + flight_list_booking[0][
            'ArrivalTime']
        root[1][0][0].attrib['Duration'] = flight_list_booking[0]['Duration']
        root[1][0][0].attrib['StopQuantity'] = flight_list_booking[0]['StopQuantity']
        root[1][0][0].attrib['RPH'] = flight_list_booking[0]['RPH']
        root[1][0][0][0].attrib['LocationCode'] = flight_list_booking[0]['origin']
        root[1][0][0][1].attrib['LocationCode'] = flight_list_booking[0]['destination']
        root[1][0][0][2].attrib['Code'] = flight_list_booking[0]['OperatingAirline']
        root[1][0][0][3].attrib['AirEquipType'] = flight_list_booking[0]['AirEquipType']
        root[1][0][0][4][0].attrib['ResBookDesigCode'] = flight_list_booking[0]['ResBookDesigCode']
        root[1][0][0][4][0].attrib['ResBookDesigQuantity'] = flight_list_booking[0]['ResBookDesigQuantity']
        n = 0
        for PTC_FB in PTC_FBs:
            if n > 0:
                membern_1 = root[2][n - 1]
                membern = deepcopy(membern_1)
                root[2].append(membern)

            root[2][n].text = PTC_FB['FareBasisCode']
            root[2][n].attrib['FlightSegmentRPH'] = PTC_FB['FareBasisCode_FlightSegmentRPH']
            root[2][n].attrib['fareRPH'] = PTC_FB['FareBasisCode_fareRPH']
            n = n + 1

    elif selected_operation_number == 4:
        root[1].attrib['DirectionInd'] = "OneWay"
        root[1][0][0][0].attrib['FlightNumber'] = flight_list_booking[0]['FlightNumber']
        root[1][0][0][0].attrib['ResBookDesigCode'] = flight_list_booking[0]['ResBookDesigCode']
        root[1][0][0][0].attrib['DepartureDateTime'] = flight_list_booking[0]['departureDate'] + 'T' + \
                                                       flight_list_booking[0]['departureTime']
        root[1][0][0][0].attrib['ArrivalDateTime'] = flight_list_booking[0]['ArrivalDate'] + 'T' + \
                                                     flight_list_booking[0]['ArrivalTime']
        root[1][0][0][0].attrib['Duration'] = flight_list_booking[0]['Duration']
        root[1][0][0][0].attrib['StopQuantity'] = flight_list_booking[0]['StopQuantity']
        root[1][0][0][0].attrib['RPH'] = flight_list_booking[0]['RPH']
        root[1][0][0][0][0].attrib['LocationCode'] = flight_list_booking[0]['origin']
        root[1][0][0][0][1].attrib['LocationCode'] = flight_list_booking[0]['destination']
        root[1][0][0][0][2].attrib['Code'] = flight_list_booking[0]['OperatingAirline']
        root[1][0][0][0][3].attrib['AirEquipType'] = flight_list_booking[0]['AirEquipType']
        root[1][0][0][0][4][0].attrib['ResBookDesigCode'] = flight_list_booking[0]['ResBookDesigCode']
        root[1][0][0][0][4][0].attrib['ResBookDesigQuantity'] = flight_list_booking[0]['ResBookDesigQuantity']
        root[2][0][0].attrib['CurrencyCode'] = flight_list_booking[0]['BaseFare_CurrencyCode']
        root[2][0][0].attrib['DecimalPlaces'] = flight_list_booking[0]['BaseFare_DecimalPlaces']
        root[2][0][0].attrib['Amount'] = flight_list_booking[0]['BaseFare_Amount']
        root[2][0][1].attrib['CurrencyCode'] = flight_list_booking[0]['TotalFare_CurrencyCode']
        root[2][0][1].attrib['DecimalPlaces'] = flight_list_booking[0]['TotalFare_DecimalPlaces']
        root[2][0][1].attrib['Amount'] = flight_list_booking[0]['TotalFare_Amount']

        i = 0

        for passenger in passengers:
            if i > 0:
                memberi_1 = root[3][i - 1]
                memberi = deepcopy(memberi_1)
                root[3].append(memberi)
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

            i = i + 1

        root[4][0][0].text = ContactGivenName
        root[4][0][1].text = ContactSureName
        root[4][1].attrib['PhoneNumber'] = Telephone
        root[4][2].attrib['PhoneNumber'] = HomeTelephone
        root[4][3].text = Email
        root[5][0][0].attrib['PaymentType'] = "2"
        root[5][0][0][0].attrib['DirectBill_ID'] = "THRTA023"
        root[5][0][0][0][0].attrib['CompanyShortName'] = "HOMARES OTA"
        root[5][0][0][0][0].attrib['Code'] = "THRTA023"
        root[5][0][0][1].attrib['CurrencyCode'] = flight_list_booking[0]['TotalFare_CurrencyCode']
        root[5][0][0][1].attrib['DecimalPlaces'] = flight_list_booking[0]['TotalFare_DecimalPlaces']
        root[5][0][0][1].attrib['Amount'] = flight_list_booking[0]['TotalFare_Amount']

    elif selected_operation_number == 5:
        root[1].attrib['ID'] = 'VPTF21'

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
                departureTime = DepartureDateTime[1].replace("+04", "+03")
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
                        'FareBasisCode': FareBasisCode,
                        'FareBasisCode_FlightSegmentRPH': FareBasisCode_FlightSegmentRPH,
                        'FareBasisCode_fareRPH': FareBasisCode_fareRPH,
                        'PassengerFare_BaseFare_CurrencyCode': PassengerFare_BaseFare_CurrencyCode,
                        'PassengerFare_BaseFare_DecimalPlaces': PassengerFare_BaseFare_DecimalPlaces,
                        'PassengerFare_BaseFare_Amount': PassengerFare_BaseFare_Amount,
                        'Taxes': Taxes,
                    })

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

    elif selected_operation_number == 3:
        global operation_three_RS
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
        passengers.clear()

    elif selected_operation_number == 5:
        root[1].attrib['ID'] = 'VPTF21'


def data_handle(selected_operation_number):
    Agent_id = 'MOW07603'
    Operation, Request_Schema, Response_Schema, Resource = source_table()
    for index, oper in enumerate(Operation, 1):
        print(str(index) + '-' + oper)
    # selected_operation_number = int(input('Select related operation number:'))
    # selected_operation_number = 2
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
