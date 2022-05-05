import json
from django.shortcuts import render


# load API
with open('/home/sepehr/Desktop/working-with-api/backend/apihandler/flight.json', 'r') as json_file:
    json_load = json.load(json_file)


def index(request):
    data = json_load  # load JSON
    origin = request.POST.get("origin")  # get flight origin from template input
    destination = request.POST.get("destination")  # get flight destination from template input
    departureTime = request.POST.get("departureTime")  # get flight departureTime from template input
    peopleNumber = request.POST.get("peopleNumber")  # get number of people from template input

    data_list = []

    # when user clicks on the submit button of form
    if request.method == 'POST':
        for data1 in data:  # turn in JSON data
            date1 = data1["departureTime"].split('T')  # split date and time from template input
            if (origin.casefold() in data1["origin"].casefold()) and (destination.casefold() in data1["destination"].casefold()) \
                    and (departureTime in date1) and (
                    int(peopleNumber) <= data1["capacity"]):  # check if inputs are in JSON data
                data_list.append({
                    'origin': data1["origin"],
                    'destination': data1["destination"],
                    'departureTime': data1["departureTime"],
                    'capacity': data1["capacity"],
                    'flightNumber': data1["flight-number"],
                    'airplane': data1["airplane"]
                })  # add result to results
            elif (origin.casefold() in data1["origin"].casefold()) and (destination.casefold() in data1["destination"].casefold()) \
                    and (not departureTime) and (not peopleNumber):  # for inputs without date and number of people
                data_list.append({
                    'origin': data1["origin"],
                    'destination': data1["destination"],
                    'departureTime': data1["departureTime"],
                    'capacity': data1["capacity"],
                    'flightNumber': data1["flight-number"],
                    'airplane': data1["airplane"]
                })

    # send data to template
    context = {
        'data_list': data_list,  # for results
        'peopleNumber': peopleNumber,  # for number of people which is in popup
        'origin': origin,  # for nothing found result
        'destination': destination,  # for nothing found result
    }
    return render(request, './Home.html', context)
