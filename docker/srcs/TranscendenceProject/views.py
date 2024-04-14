from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
#from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'index.html')
