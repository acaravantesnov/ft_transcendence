'''
A view function is a function that takes a Request and returns a Response. It is a Request Handler.
In sime frameworks it is called an action, but in Django it is called a view.
'''

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.http import HttpResponse, JsonResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

'''
REST framework provides an APIView class, which subclasses Django's View class.

APIView classes are different from regular View classes in the following ways:

* Requests passed to the handler methods will be REST framework's Request instances, not Django's
HttpRequest instances.
* Handler methods may return REST framework's Response, instead of Django's HttpResponse. The view
will manage content negotiation and setting the correct renderer on the response.
* Any APIException exceptions will be caught and mediated into appropriate responses.
* Incoming requests will be authenticated and appropriate permission and/or throttle checks will be
run before dispatching the request to the handler method.
'''
from rest_framework.response import Response

'''
REST framework also allows you to work with regular function based views. It provides a set of
simple decorators that wrap your function based views to ensure they receive an instance of Request
(rather than the usual Django HttpRequest) and allows them to return a Response (instead of a Django
HttpResponse), and allow you to configure how the request is processed.

The core of this functionality is the api_view decorator, which takes a list of HTTP methods that
your view should respond to.
'''
from rest_framework.decorators import api_view


from .serializers import MyCustomUserSerializer, GameSerializer
from .models import *
from .forms import signUser, newUser
from .waiting_room import waiting_room

import logging

logger = logging.getLogger("views")


# Normal views

def title(request):
    if request.user.is_authenticated:
        return render(request, 'title.html')
    return redirect('home', username='Guest')

def home(request, username):
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'title.html')
    form = signUser()
    return render(request, 'signIn.html', {'form': form})

def waitlist(request, username):
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'waitlist.html')
    form = signUser()
    return render(request, 'signIn.html', {'form': form})

def play(request, username, room_name, side):
    logger.debug(f" [views] play: {username}, {room_name}, {side} ")
    return render(request, 'game.html', {"username": username, "room_name": room_name, "side": side})

def leaderboards(request, username):
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'leaderboards.html')
    form = signUser()
    return render(request, 'signIn.html', {'form': form})

def profile(request, username):
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'profile.html')
    form = signUser()
    return render(request, 'signIn.html', {'form': form})

def signUp(request):
    form = newUser()
    return render(request, "signUp.html", {"form": form})


# CRUD API views

@api_view(['POST'])
def createUser(request):
    request.data['password'] = make_password(request.data['password'])
    
    serializer = MyCustomUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': serializer.errors})

@api_view(['GET'])
def readUser(request, pk):
    users = MyCustomUser.objects.get(id=pk)
    serializer = MyCustomUserSerializer(users, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateUser(request, pk):
    user = MyCustomUser.objects.get(id=pk)
    serializer = MyCustomUserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, pk):
    user = MyCustomUser.objects.get(id=pk)
    user.delete()
    return Response('User successfully deleted!')


# API GET views

@api_view(['GET'])
def getUserInfo(request):
    if request.user.is_authenticated:
        try:
            user = MyCustomUser.objects.get(username=request.user.username)
            return JsonResponse({
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'last_login': user.last_login,
                'date_joined': user.date_joined,
                'avatar': user.avatar.url,
            })
        except MyCustomUser.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    else:
        return JsonResponse({
            'username': 'Guest',
            'first_name': 'Guest',
            'last_name': 'Guest',
            'email': 'Guest',
            'last_login': 'Guest',
            'date_joined': 'Guest',
            'avatar': '/media/avatars/default.png',
        })
        
@api_view(['GET'])
def statistics(request, username):
    if (MyCustomUser.objects.filter(username=username).count() == 0):
        return Response({'error': 'User not found'})
    games = Game.objects.filter(player1__username=username) | Game.objects.filter(player2__username=username)
    gamesWon = games.filter(winner__username=username)
    gamesLost = games.exclude(winner__username=username)
    goals = 0
    for game in games:
        if game.player1.username == username:
            goals += game.player1_score
        else:
            goals += game.player2_score
    return Response({'gamesWon': gamesWon.count(), 'gamesLost': gamesLost.count(), 'goals': goals})

@api_view(['GET'])
def checkwaitlist(request, username):
    response = waiting_room.user_check_if_waiting_is_done(username)
    logger.debug(f" [views] checkwaitlist: {response} ")
    if response is None:
        return JsonResponse({'status': 'waiting'})
    return JsonResponse({'status': 'success', 'response': response})


# API POST views

@api_view(['POST'])
def addGame(request):
    request.data['player1'] = MyCustomUser.objects.get(username=request.data['player1']).pk
    request.data['winner'] = MyCustomUser.objects.get(username=request.data['winner']).pk
    serializer = GameSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)

@api_view(['POST'])
def checkCredentials(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    try:
        user = MyCustomUser.objects.get(username=username)
    except MyCustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})

    if not user.is_active:
        user.is_active = True
        user.save()
        print(f"Activated user '{username}'")
    
    
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Username or Password', 'username': username})

@api_view(['POST'])
def signOut(request):
    auth.logout(request)
    return JsonResponse({'status': 'success'})

@api_view(['POST'])
def addtowaitlist(request, username):
    logger.debug(f" [views] addtowaitlist: {username} ")
    waiting_room.add_user(username)
    return JsonResponse({'status': 'success'})


# API unused views

@api_view(['GET'])
def getData(request):
    users = MyCustomUser.objects.all()
    serializer = MyCustomUserSerializer(users, many=True)
    return Response(serializer.data)

    