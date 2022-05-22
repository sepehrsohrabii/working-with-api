from django.shortcuts import render
import requests
from pathlib import Path
import re
from datetime import datetime


context = {}
flight_list = []
PTC_FBs = []
Taxes = []

def index(request):
    # data = json_load  # load JSON
    selected_operation_number = 2
    global origin
    global destination
    global departureTime
    global ADTNumber
    global CHDNumber
    global INFNumber
    global Cabin
    origin = request.POST.get("origin")  # get flight origin from template input
    destination = request.POST.get("destination")  # get flight destination from template input
    departureTime = request.POST.get("departureTime")  # get flight departureTime from template input
    ADTNumber = request.POST.get("ADTNumber")  # get number of people from template input
    CHDNumber = request.POST.get("CHDNumber")  # get number of people from template input
    INFNumber = request.POST.get("INFNumber")  # get number of people from template input
    Cabin = request.POST.get("Cabin")  # get number of people from template input
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
    context = {
        'data_list': data_list,  # for results
        'ADTNumber': ADTNumber,  # for number of Adults which is in popup
        'CHDNumber': CHDNumber,  # for number of Children which is in popup
        'INFNumber': INFNumber,  # for number of Babies which is in popup
        'origin': origin,  # for nothing found result
        'destination': destination,  # for nothing found result
        'departureTime': departureTime,
    }

    return render(request, './Home.html', context)

def buypage(request, FlightNumber):
    Operation, Request_Schema, Response_Schema, Resource = source_table()
    global flight_list_booking
    flight_list_booking = []
    global passengers
    passengers = []
    selected_operation_number = 2
    selected_Response_Schema = Response_Schema[selected_operation_number - 1]
    respath = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(selected_Response_Schema[:-4])
    import xml.etree.ElementTree as ET
    tree = ET.parse(respath)
    root = tree.getroot()
    for PricedItinerary in root[1]:
        FlightSegment = PricedItinerary[0][0][0][0]
        FlightNumberSRS = FlightSegment.attrib['FlightNumber']
        if FlightNumberSRS in FlightNumber:
            SequenceNumber = PricedItinerary.attrib['SequenceNumber']
            ResBookDesigCode = FlightSegment.attrib['ResBookDesigCode']
            DepartureDateTime = FlightSegment.attrib['DepartureDateTime'].split('T')
            departureDate = DepartureDateTime[0]
            departureTime = DepartureDateTime[1]
            ArrivalDateTime = FlightSegment.attrib['ArrivalDateTime'].split('T')
            ArrivalDate = ArrivalDateTime[0]
            ArrivalTime = ArrivalDateTime[1]
            Duration = FlightSegment.attrib['Duration']
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
                    'PassengerTypeQuantity_Range': range(1, int(PassengerTypeQuantity_Quantity)+1),
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

    for item in range(1, int(ADTNumber)+1):
        NamePrefix_str = "NamePrefix" + str(item) + "ADT"
        NamePrefix = request.POST.get(NamePrefix_str)
        GivenName_str = "GivenName" + str(item) + "ADT"
        GivenName = request.POST.get(GivenName_str)
        SureName_str = "SureName" + str(item) + "ADT"
        SureName = request.POST.get(SureName_str)
        BirthDate_str = "BirthDate" + str(item) + "ADT"
        BirthDate = request.POST.get(BirthDate_str)
        Gender_str = "Gender" + str(item) + "ADT"
        Gender = request.POST.get(Gender_str)
        TravelerNationality_str = "TravelerNationality" + str(item) + "ADT"
        TravelerNationality = request.POST.get(TravelerNationality_str)
        DocID_str = "DocID" + str(item) + "ADT"
        DocID = request.POST.get(DocID_str)
        passengers.append({
            'NamePrefix': NamePrefix,
            'GivenName': GivenName,
            'SureName': SureName,
            'BirthDate': BirthDate,
            'Gender': Gender,
            'TravelerNationality': TravelerNationality,
            'DocID': DocID
        })
    for item in range(1, int(CHDNumber)+1):
        NamePrefix_str = "NamePrefix" + str(item) + "CHD"
        NamePrefix = request.POST.get(NamePrefix_str)
        GivenName_str = "GivenName" + str(item) + "CHD"
        GivenName = request.POST.get(GivenName_str)
        SureName_str = "SureName" + str(item) + "CHD"
        SureName = request.POST.get(SureName_str)
        BirthDate_str = "BirthDate" + str(item) + "CHD"
        BirthDate = request.POST.get(BirthDate_str)
        Gender_str = "Gender" + str(item) + "CHD"
        Gender = request.POST.get(Gender_str)
        TravelerNationality_str = "TravelerNationality" + str(item) + "CHD"
        TravelerNationality = request.POST.get(TravelerNationality_str)
        DocID_str = "DocID" + str(item) + "CHD"
        DocID = request.POST.get(DocID_str)
        passengers.append({
            'NamePrefix': NamePrefix,
            'GivenName': GivenName,
            'SureName': SureName,
            'BirthDate': BirthDate,
            'Gender': Gender,
            'TravelerNationality': TravelerNationality,
            'DocID': DocID
        })
    for item in range(1, int(INFNumber)+1):
        NamePrefix_str = "NamePrefix" + str(item) + "INF"
        NamePrefix = request.POST.get(NamePrefix_str)
        GivenName_str = "GivenName" + str(item) + "INF"
        GivenName = request.POST.get(GivenName_str)
        SureName_str = "SureName" + str(item) + "INF"
        SureName = request.POST.get(SureName_str)
        BirthDate_str = "BirthDate" + str(item) + "INF"
        BirthDate = request.POST.get(BirthDate_str)
        Gender_str = "Gender" + str(item) + "INF"
        Gender = request.POST.get(Gender_str)
        TravelerNationality_str = "TravelerNationality" + str(item) + "INF"
        TravelerNationality = request.POST.get(TravelerNationality_str)
        DocID_str = "DocID" + str(item) + "INF"
        DocID = request.POST.get(DocID_str)
        passengers.append({
            'NamePrefix': NamePrefix,
            'GivenName': GivenName,
            'SureName': SureName,
            'BirthDate': BirthDate,
            'Gender': Gender,
            'TravelerNationality': TravelerNationality,
            'DocID': DocID
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

    if request.method == 'POST':
        selected_operation_number = 4
        #data_handle(selected_operation_number)

    buy_context = {
        'flight_list_booking': flight_list_booking,
    }
    return render(request, './buypage.html', buy_context)

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
    #print('you select %s' % selected_operation)
    selected_Request_Schema = Request_Schema[selected_operation_number - 1]

    path = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}.xml'.format(
        selected_Request_Schema[:-4])
    newpath = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(
        selected_Request_Schema[:-4])
    import xml.etree.ElementTree as ET
    tree = ET.parse(path)
    root = tree.getroot()
    root[0][0][0].attrib['ID'] = Agent_id
    root[0][0].attrib['ISOCurrency'] = 'RUB'
    root.attrib['Target'] = 'Test'  # Test or Production
    root.attrib['TimeStamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    root.attrib['EchoToken'] = '0001'
    if selected_operation_number == 1:
        root[1].text = 'Hi sepehr'
    elif selected_operation_number == 2:
        if departureTime != '':
            root[1][0].text = departureTime
        else:
            root[1][0].text = ''

        if origin != '':
            root[1][1].attrib['LocationCode'] = origin
        else:
            root[1][1].attrib['LocationCode'] = ''

        if destination != '':
            root[1][2].attrib['LocationCode'] = destination
        else:
            root[1][2].attrib['LocationCode'] = ''

        if ADTNumber != '':
            root[3][0][0].attrib['Quantity'] = ADTNumber
        else:
            root[3][0][0].attrib['Quantity'] = '0'

        if CHDNumber != '':
            root[3][0][1].attrib['Quantity'] = CHDNumber
        else:
            root[3][0][1].attrib['Quantity'] = '0'

        if INFNumber != '':
            root[3][0][2].attrib['Quantity'] = INFNumber
        else:
            root[3][0][2].attrib['Quantity'] = '0'

        if Cabin != '':
            root[2][0].attrib['Cabin'] = Cabin
        else:
            root[2][0].attrib['Cabin'] = ''


    elif selected_operation_number == 3:
        root[1][0].text = '2022-05-10'


    elif selected_operation_number == 4:
        root[1].attrib['DirectionInd'] = "OneWay"
        root[1][0][0][0].attrib['FlightNumber'] = flight_list_booking[0]['FlightNumber']
        root[1][0][0][0].attrib['ResBookDesigCode'] = "X"
        root[1][0][0][0].attrib['DepartureDateTime'] = flight_list_booking[0]['departureDate']+'T'+flight_list_booking[0]['departureTime']
        root[1][0][0][0].attrib['ArrivalDateTime'] = flight_list_booking[0]['ArrivalDate']+'T'+flight_list_booking[0]['ArrivalTime']
        root[1][0][0][0].attrib['Duration'] = flight_list_booking[0]['Duration']
        root[1][0][0][0].attrib['StopQuantity'] = flight_list_booking[0]['StopQuantity']
        root[1][0][0][0].attrib['RPH'] = flight_list_booking[0]['RPH']
        root[1][0][0][0][0].attrib['LocationCode'] = flight_list_booking[0]['origin']
        root[1][0][0][0][1].attrib['LocationCode'] = flight_list_booking[0]['destination']
        root[1][0][0][0][2].attrib['Code'] = flight_list_booking[0]['OperatingAirline']
        root[1][0][0][0][3].attrib['AirEquipType'] = flight_list_booking[0]['AirEquipType']
        root[1][0][0][0][4][0].attrib['ResBookDesigCode'] = "X"
        root[1][0][0][0][4][0].attrib['ResBookDesigQuantity'] = flight_list_booking[0]['ResBookDesigQuantity']

        root[2][0][0].attrib['CurrencyCode'] = flight_list_booking[0]['BaseFare_CurrencyCode']
        root[2][0][0].attrib['DecimalPlaces'] = flight_list_booking[0]['BaseFare_DecimalPlaces']
        root[2][0][0].attrib['Amount'] = flight_list_booking[0]['BaseFare_Amount']
        root[2][0][1].attrib['CurrencyCode'] = flight_list_booking[0]['TotalFare_CurrencyCode']
        root[2][0][1].attrib['DecimalPlaces'] = flight_list_booking[0]['TotalFare_DecimalPlaces']
        root[2][0][1].attrib['Amount'] = flight_list_booking[0]['TotalFare_Amount']
        i = 0
        for PTC_FB in flight_list_booking[0]['PTC_FBs']:
            root[3][i].attrib['BirthDate'] = "1974-04-16"
            root[3][i].attrib['PassengerTypeCode'] = "ADT"
            root[3][i].attrib['AccompaniedByInfantInd'] = "false"
            root[3][i].attrib['Gender'] = "M"
            root[3][i].attrib['TravelerNationality'] = "IR"

            root[3][i][0][0].text = "MR"
            root[3][i][0][1].text = "SAEID"
            root[3][i][0][2].text = "NAZKASRAEI"

            root[3][i][1].attrib['RPH'] = "1"

            root[3][i][2].attrib['DocID'] = "1121234545"
            root[3][i][2].attrib['DocType'] = "5"
            root[3][i][2].attrib['DocIssueCountry'] = "IR"

            i = i + 1

        root[4][0][0].text = "SEPEHR"
        root[4][0][1].text = "SOHRABI"

        root[4][1].attrib['PhoneNumber'] = "(98)2232343212"
        root[4][2].attrib['PhoneNumber'] = "(98)2132343212"

        root[4][3].text = "tbacon@tba.com"

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

    import xml.etree.ElementTree as ET
    tree = ET.parse(respath)
    root = tree.getroot()

    if selected_operation_number == 1:
        root[1].text = 'Hi sepehr'

    elif selected_operation_number == 2:
        if 'Success' in root[0].tag:
            for PricedItinerary in root[1]:
                SequenceNumber = PricedItinerary.attrib['SequenceNumber']
                FlightSegment = PricedItinerary[0][0][0][0]
                FlightNumber = FlightSegment.attrib['FlightNumber']
                ResBookDesigCode = FlightSegment.attrib['ResBookDesigCode']
                DepartureDateTime = FlightSegment.attrib['DepartureDateTime'].split('T')
                departureDate = DepartureDateTime[0]
                departureTime = DepartureDateTime[1]
                ArrivalDateTime = FlightSegment.attrib['ArrivalDateTime'].split('T')
                ArrivalDate = ArrivalDateTime[0]
                ArrivalTime = ArrivalDateTime[1]
                Duration = FlightSegment.attrib['Duration']
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
        root[1][0].text = '2022-05-10'


    elif selected_operation_number == 4:
        return

    elif selected_operation_number == 5:
        root[1].attrib['ID'] = 'VPTF21'


def data_handle(selected_operation_number):
    Agent_id = 'MOW07603'

    Operation, Request_Schema, Response_Schema, Resource = source_table()

    for index, oper in enumerate(Operation, 1):
        print(str(index) + '-' + oper)
    #selected_operation_number = int(input('Select related operation number:'))
    #selected_operation_number = 2
    selected_Response_Schema = Response_Schema[selected_operation_number - 1]
    selected_Resource = Resource[selected_operation_number - 1]

    headers = {'Accept': 'application/xml',
               'Content-Type': 'application/xml',
               'Authorization': 'y00Lm/iuKNN6X8xU/p5FyJYVjXBCOh/JEQdcwPyGtJg='}
    endpoint = 'https://staging.homares.ir/wsbe/rest'

    url = endpoint + selected_Resource

    xmlfile = write_on_xml(selected_operation_number)

    response = requests.post(url=url, data=xmlfile, headers=headers)
    respath = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(selected_Response_Schema[:-4])

    with open(respath, 'w') as f:
        f.write(response.text)
    f.close()

    read_from_xml(selected_operation_number, respath)