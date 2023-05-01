from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm


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
                messages.success(
                    request, ('Welcome back you have been logged in!'))
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
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('You are now registered'))
            return redirect('home')

    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'authenicate/register.html', context)


def edit_profile(request):
    form = None  # define form variable and set it to None
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ('You have updated your profile'))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'authenicate/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            update_session_auth_hash(request, user)  # Important!
            return redirect('change_password')
        else:
            messages.error(request, 'Please try again.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authenicate/change_password.html', {'form': form})


