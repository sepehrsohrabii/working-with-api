from django.shortcuts import render
from search_data.models import SearchData
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(redirect_field_name='next', login_url='/accounts/login')
def AdminPanel(request):
    searched_data = SearchData.objects.all()
    
    return render(request, './panel.html', {'searched_data': searched_data})