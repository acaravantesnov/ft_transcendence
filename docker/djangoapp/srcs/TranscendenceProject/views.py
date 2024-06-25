'''
A view function is a function that takes a Request and returns a Response. It is a Request Handler.
In sime frameworks it is called an action, but in Django it is called a view.
'''

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth

def welcome(request):
    username = request.user.username
    return render(request, 'index.html', {'username': username})

def error404(request):
    return render(request, '404.html')
