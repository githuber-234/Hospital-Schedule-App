from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


def home(request):
    return render(request, 'Users/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.role == 'doctor':
                    messages.success(request, "Welcome!")
                    return redirect('doctor')
                elif user.role == 'patient':
                    messages.success(request, "Welcome!")
                    return redirect('patient')
                else:
                    return redirect('default_dashboard')
            else:
                return redirect('login')
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})