from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from accounts.models import UserInfo
from django.contrib.auth import authenticate, login, logout
from apihandler.views import home_page


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        redirect_to = request.POST.get('next', '')
        if request.method == 'POST':
            userName = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=userName, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if redirect_to != '':
                    return HttpResponseRedirect(redirect_to)
                else:
                    return redirect('home_page')

    return render(request, './login.html', locals())



def signupView(request):
    redirect_to = request.POST.get('next', '')
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        userName= email
        phoneNumber = request.POST.get('phoneNumber')
        password = request.POST.get('password')

        user = User.objects.create_user(str(userName), str(email), str(password))
        user.first_name = firstName
        user.last_name = lastName

        user.save()
        user = authenticate(request, username=userName, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            data = UserInfo()
            data.user = current_user
            data.phone = phoneNumber
            data.save()
            if redirect_to != '':
                return HttpResponseRedirect(redirect_to)
            else:
                return redirect('home_page')

    return render(request, './signup.html')

def logoutView(request):
    logout(request)
    
    return redirect('/accounts/login/')

def userProfile(request):

    return render(request, './profile.html')
