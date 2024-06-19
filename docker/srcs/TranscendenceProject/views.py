'''
A view function is a function that takes a Request and returns a Response. It is a Request Handler.
In sime frameworks it is called an action, but in Django it is called a view.
'''

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
#from django.http import HttpResponse

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "Guest"
    return render(request, 'index.html')

def error404(request):
    return render(request, '404.html')
