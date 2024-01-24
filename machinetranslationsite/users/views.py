from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from . forms import UserRegisterForm


# Create your views here.

def home(request):
    return render(request, 'users/home.html')


def login(request):
    return render(request, 'users/login.html')

def logout(request):
    return render(request, 'users/logout.html')


def register(request):
    form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully.')
            return redirect(reverse('site:home'))

    return render(request, 'users/register.html', {'form': form})