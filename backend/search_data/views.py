from django.shortcuts import render
from search_data.models import SearchData


def save_search_data(request):
    data1 = SearchData()
    data1.a = 'a'
    data1.b = '2022-07-06 00:00:00'
    data1.c = 'd'
    data1.d = 1
    data1.e = 2
    data1.f = 3
    data1.save()
    return render(request, './datashow.html')
