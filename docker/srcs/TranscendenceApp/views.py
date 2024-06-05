'''
A view function is a function that takes a Request and returns a Response. It is a Request Handler.
In sime frameworks it is called an action, but in Django it is called a view.
'''

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.http import HttpResponse

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


from .serializers import UserSerializer, GameSerializer
from .models import MyCustomUser, Game
from .forms import signUser, newUser

import logging

logger = logging.getLogger("views")

@api_view(['GET'])
def getData(request):
    users = MyCustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    users = MyCustomUser.objects.get(id=pk)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['PUT'])
def updateUser(request, pk):
    user = MyCustomUser.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, pk):
    user = MyCustomUser.objects.get(id=pk)
    user.delete()
    return Response('User successfully deleted!')

def signUp(request):
    form = newUser(request.POST)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            if password == confirm_password:
                if MyCustomUser.objects.filter(username=username).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('signUp')
                else:
                    user = MyCustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.set_password(password)
                    user.save()
                    print("success")
                    return redirect('signIn')
    else:
        print('This is not post method')
        return render(request, "signUp.html", {"form": form})

def signIn(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, "signIn.html", {"username": username})
    else:
        form = signUser(request.POST or None)
        if request.method == "POST":
            if  form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                    auth.login(request,user)
                    return redirect('signed', username=username)
                else:
                    messages.info(request, 'Invalid Username or Password')
                    return redirect('signIn')
        else:        
            return render(request, "signIn.html", {"form": form})

def signed(request, username):
    return render(request, "signed.html", {"username": username})

def logOut(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('index')

def game(request):
    return render(request, "game.html")

def game2(request, room_name):
    logger.debug(f'room_name: {room_name}')
    return render(request, "game2.html", {'room_name': room_name})

