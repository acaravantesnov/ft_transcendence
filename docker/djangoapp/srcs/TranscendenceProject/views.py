'''
A view function is a function that takes a Request and returns a Response. It is a Request Handler.
In sime frameworks it is called an action, but in Django it is called a view.
'''

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
from TranscendenceApp.translations import translate

def welcome(request):
    lang = request.session.get('lang_code', 'es')
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    username = request.user.username
    context = {
        'username': username,
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    return render(request, 'index.html', context)
