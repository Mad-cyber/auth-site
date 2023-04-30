from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def home(request):
    return render(request, 'authenicate/home.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is not None and password is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ('Welcome back you have been logged in!'))
                return redirect('home')
            else:
                messages.success(
                    request, ('Error Logging In - Please try Again!'))
        # Handle the case where username or password is missing
        return redirect('loginpage')
    else:
        return render(request, 'authenicate/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ('You have logged out sucessfully'))
    return redirect ('home')

def register_user(request):
     if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             username = form.cleaned_data['username']
             password = form.cleaned_data['password1']
             user = authenticate(request, username=username, password=password)
             login(request, user)
             messages.success(request, ('You are now registered'))
             return redirect('home')

     else:
         form = UserCreationForm()
     context = {'form': form}    
     return render(request, 'authenicate/register.html', context)