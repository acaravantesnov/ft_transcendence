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

import logging

logger = logging.getLogger("views")

@api_view(['GET'])
def getCurrentUsername(request):
    if (request.user.is_authenticated):
        return JsonResponse({'username': request.user.username})
    else:
        return JsonResponse({'username': 'Guest'})

@api_view(['GET'])
def getData(request):
    users = MyCustomUser.objects.all()
    serializer = MyCustomUserSerializer(users, many=True)
    return Response(serializer.data)

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
        return JsonResponse({'status': 'error', 'message': 'Invalid Username or Password'})

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

def title(request):
    return render(request, 'title.html')

def home(request, username):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "Guest"
    return render(request, 'index.html', {"username": username})

def signIn(request):
    if request.user.is_authenticated:
        return redirect('/users/game/' + request.user.username)
    form = signUser()
    return render(request, "signIn.html", {"form": form})

def signUp(request):
    form = newUser()
    return render(request, "signUp.html", {"form": form})

def signOut(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request, 'title.html')

def game(request, username):
    return render(request, 'game.html', {"username": username})