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
    selected_operation_number = 2
    global origin
    global destination
    global departureTime
    global return_date
    global ADTNumber
    global CHDNumber
    global INFNumber
    global Cabin
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
    return render(request, './operation_two.html', operation_two_data)


def operation_three(request, FlightNumber):
    selected_operation_number = 3
    selected_flight.clear()
    for Flight in flight_list:
        if Flight['FlightNumber'] == FlightNumber:
            selected_flight.append(Flight)
            flight_list.clear()

    data_handle(selected_operation_number)
    '''
    if 'return_date' in selected_flight[0]:
        selected_operation_number = 3
        data_handle(selected_operation_number)
    '''
    return render(request, './operation_three.html', operation_three_RS)


def operation_four(request):
    passengers.clear()
    Error.clear()
    flight_list.clear()
    submit = request.POST.get('submit')
    if submit:
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

    return render(request, './operation_four.html', {'selected_flight': selected_flight, 'Error': Error})
