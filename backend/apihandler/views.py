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
    flight_list_booking = []
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


    print(FlightNumber)
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
        # print(Request_Schema[2])
        search_path = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(Response_Schema[1][:-4])
        import xml.etree.ElementTree as ET
        search_tree = ET.parse(search_path)
        search_root = search_tree.getroot()
        
        for el in search_tree.iter():
            for key in el.attrib.keys():
                if key == 'FlightNumber':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['FlightNumber'] = el.attrib[key]
                if key == 'DepartureDateTime':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['DepartureDateTime'] = el.attrib[key]
                if key == 'ArrivalDateTime':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['ArrivalDateTime'] = el.attrib[key]
                if key == 'Duration':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['Duration'] = el.attrib[key]
                if key == 'StopQuantity':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['StopQuantity'] = el.attrib[key]
                if key == 'RPH':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'AirEquipType':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['AirEquipType'] = el.attrib[key]
                if key == 'RPH':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]

        # print(search_root[1][0][1][0][0].attrib['Amount'])
        # print(search_root[1][0][1][0][1].attrib['Amount'])

        root[2][0][0].attrib['Amount'] = search_root[1][0][1][0][0].attrib['Amount']
        root[2][0][1].attrib['Amount'] = search_root[1][0][1][0][1].attrib['Amount']
        root[2][0][0].attrib['CurrencyCode'] = search_root[1][0][1][0][0].attrib['CurrencyCode']
        root[2][0][1].attrib['CurrencyCode'] = search_root[1][0][1][0][1].attrib['CurrencyCode']
        root[5][0][0][1].attrib['Amount'] = search_root[1][0][1][0][1].attrib['Amount']
        root[5][0][0][1].attrib['CurrencyCode'] = search_root[1][0][1][0][1].attrib['CurrencyCode']



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
        # print(Request_Schema[2])
        search_path = '/home/sepehr/Desktop/working-with-api/backend/apihandler/data/HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(Response_Schema[1][:-4])
        import xml.etree.ElementTree as ET
        search_tree = ET.parse(search_path)
        search_root = search_tree.getroot()
        for el in search_tree.iter():
            for key in el.attrib.keys():
                if key == 'FlightNumber':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['FlightNumber'] = el.attrib[key]
                if key == 'DepartureDateTime':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['DepartureDateTime'] = el.attrib[key]
                if key == 'ArrivalDateTime':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['ArrivalDateTime'] = el.attrib[key]
                if key == 'Duration':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['Duration'] = el.attrib[key]
                if key == 'StopQuantity':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['StopQuantity'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'AirEquipType':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['AirEquipType'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]

        # print(search_root[1][0][1][0][0].attrib['Amount'])
        # print(search_root[1][0][1][0][1].attrib['Amount'])

        root[2][0][0].attrib['Amount'] = search_root[1][0][1][0][0].attrib['Amount']
        root[2][0][1].attrib['Amount'] = search_root[1][0][1][0][1].attrib['Amount']
        root[2][0][0].attrib['CurrencyCode'] = search_root[1][0][1][0][0].attrib['CurrencyCode']
        root[2][0][1].attrib['CurrencyCode'] = search_root[1][0][1][0][1].attrib['CurrencyCode']
        root[5][0][0][1].attrib['Amount'] = search_root[1][0][1][0][1].attrib['Amount']
        root[5][0][0][1].attrib['CurrencyCode'] = search_root[1][0][1][0][1].attrib['CurrencyCode']
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