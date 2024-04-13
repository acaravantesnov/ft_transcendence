from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
from .forms import signUser, newUser

@api_view(['GET'])
def getData(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    users = User.objects.get(id=pk)
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
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response('User successfully deleted!')


def signIn(request):
    #return render(request, '')
    form = signUser(request.POST)
    if form.is_valid():
        if form.validate():
            print("Aqui entramos")
   #     username = form.cleaned_data.get("username")
   #     password = form.cleaned_data.get("password")
   #     user = authenticate(request, username=username, password=password)
   #     #login(request, user)
   #     print(user)
   #     if not user:
   #         return HttpResponse("<h1> Vete a Parla </h2>")
   #     return redirect('signed', username)
    return render(request, "signIn.html", {'form': form})

def signUp(request):
    if request.method == "POST":
        form = newUser(request.POST)
        #if form.validate_username() and form.validate_password():
        if form.is_valid():
            form.save()
        messages.success(request, 'Registration Successfull')
        return redirect('index')
    else:
        form = newUser()

    return render(request, 'signUp.html', {'form': form})

def signed(request, username):
    return HttpResponse("<h1> Hello %s</h2>" % username)
