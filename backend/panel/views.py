from django.shortcuts import render
from search_data.models import SearchData


def AdminPanel(request):
    searched_data = SearchData.objects.all()
    
    return render(request, './panel.html', {'searched_data': searched_data})