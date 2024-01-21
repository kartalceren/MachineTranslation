from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def login(request):
    return HttpResponse("<h1>this is login view</h1>")