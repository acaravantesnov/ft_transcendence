'''
A view function is a function that takes a Request and returns a Response. It is a Request Handler.
In sime frameworks it is called an action, but in Django it is called a view.
'''

import os
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from rest_framework import status
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.utils import translation

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
from .forms import signUser, newUser, updateProfileInfo, newPassword, updateAvatarForm
from .waiting_room import waiting_room
from .tournament_manager import tournament_manager
from .translations import translate


import logging
import random

logger = logging.getLogger("views")

# Normal views

def change_language(request, lang):
    username = request.user.username
    if request.user.is_authenticated:
        request.user.preferred_language = lang
        request.user.save()
    context = {
        'username': username,
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    return render(request, 'title.html', context)

def title(request):
    username = request.user.username
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'username': username,
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    if request.headers.get('Accept') != '*/*':
        return render(request, 'index.html', context)
    if request.user.is_authenticated:
        return render(request, 'title.html', context)
    context['username'] = 'Guest'
    return redirect('home', context)

def home(request, username):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'username': username,
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
        'title_text': translate('TITLE', lang),
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        context['username'] = username
        return render(request, 'index.html', context)
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'title.html', context)
    form = signUser()
    context['form'] = form
    return render(request, 'signIn.html', context)
    

def play(request, username):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'username': username,
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
        'wait_text': translate('WAIT', lang),
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        context['username'] = username
        return render(request, 'index.html', context)
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'game.html', context)
    form = signUser()
    context['form'] = form
    return render(request, 'signIn.html', context)

def playing(request, username):
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        return render(request, 'index.html', {'username': username})
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'playing.html', {"username": username})
    form = signUser()
    return render(request, 'signIn.html', {'form': form})


def menu(request, username):
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'menu.html');
    form = signUser();
    return render(request, 'signIn.html', {'form': form})

def modeMenu(request, mode, username):
    if request.user.is_authenticated and username != 'Guest':
        return render(request, 'menu2.html');
    form = signUser();
    return render(request, 'signIn.html', {'form': form})

def profile(request, username):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'username': username,
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        context['username'] = username
        return render(request, 'index.html', context)
    if request.user.is_authenticated and username != 'Guest':
        context['profile_text'] = translate('PROFILE', lang)
        context['edit_profile_text'] = translate('EDIT_PROFILE', lang)
        context['change_pass_text'] = translate('C_PASS', lang)
        context['choose_avatar_text'] = translate('AVATAR', lang)
        return render(request, 'profile.html', context)
    form = signUser()
    context['form'] = form
    return render(request, 'signIn.html', context)

def signUp(request):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        context['username'] = username
        return render(request, 'index.html', context)
    form = newUser()
    context['form'] = form
    context['username_text'] = translate('USERNAME', lang)
    context['first_name_text'] = translate('FIRST_NAME', lang)
    context['last_name_text'] = translate('LAST_NAME', lang)
    context['email_text'] = translate('EMAIL', lang)
    context['pass_text'] = translate('PASS', lang)
    context['pass_confirmation_text'] = translate('CONF_PASS', lang)
    return render(request, "signUp.html", context)

def editProfile(request):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        context['username']= username
        return render(request, 'index.html', context)
    if request.user.is_authenticated:
        form = updateProfileInfo()
        context['form']= form
        context['your_profile_text'] = translate('Y_PROFILE', lang)
        context['username_text'] = translate('USERNAME', lang)
        context['first_name_text'] = translate('FIRST_NAME', lang)
        context['last_name_text'] = translate('LAST_NAME', lang)
        context['email_text'] = translate('EMAIL', lang)
        context['update_text'] = translate('UPDATE', lang)
    return render(request, 'editProfile.html', context)

def changePassword(request):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        context['username']= username
        return render(request, 'index.html', context)
    form = newPassword()
    context['form']= form
    context['n_pass_text']= translate('N_PASS', lang) 
    context['c_pass_text']= translate('C_PASS', lang) 
    context['r_pass_text']= translate('R_PASS', lang) 
    context['u_pass_text']= translate('U_PASS', lang) 
    return render(request, 'changePassword.html', context)

def leaderboards(request, username):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        context['username']= username
        return render(request, 'index.html', context)
    context['rank_text']= translate('RANK', lang) 
    context['username_text']= translate('USERNAME', lang) 
    context['score_text']= translate('SCORE', lang) 
    return render(request, 'leaderboards.html', context)

def friends(request, username):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    context = {
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        context['username']= username
        return render(request, 'index.html', context)
    if request.user.is_authenticated and username != 'Guest':
        context['friend_list_text']= translate('L_FRIENDS', lang) 
        context['friends_text']= translate('FRIENDS', lang) 
        context['rank_text']= translate('RANK', lang) 
        context['player_text']= translate('PLAYER', lang) 
        context['status_text']= translate('STATUS', lang) 
        return render(request, 'friends.html', context)
    form = signUser()
    context['form'] = form
    return render(request, 'signIn.html', context)

def dashboard(request, username):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    username = request.user.username
    context = {
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
        'username': username,
    }
    if request.headers.get('Accept') != '*/*':
        return render(request, 'index.html', context)
    context['won_text']= translate('WON', lang)
    context['lost_text']= translate('LOST', lang)
    context['view_stats_text']= translate('VIEW', lang)
    context['player1_text']= translate('PLAYER1', lang)
    context['player2_text']= translate('PLAYER2', lang)
    context['winner_text']= translate('WINNER', lang)
    context['date_text']= translate('DATE', lang)
    context['no_games_text']= translate('NO_GAMES', lang)
    return render(request, 'dashboard.html', context)

def stats(request, username):
    lang = 'en'
    if request.user.is_authenticated:
        lang = request.user.preferred_language
    username = request.user.username
    context = {
        'welcome_message': translate('WELCOME', lang),
        'sign_in_text': translate('SIGN_IN', lang),
        'sign_up_text': translate('SIGN_UP', lang),
        'no_account_text': translate('NO_ACCOUNT', lang),
        'play_text': translate('PLAY', lang),
        'leaderboards_text': translate('LEADERBOARDS', lang),
        'dashboard_text': translate('DASHBOARD', lang),
        'english_text': translate('ENGLISH', lang),
        'french_text': translate('FRENCH', lang),
        'spanish_text': translate('SPANISH', lang),
        'username': username,
    }
    if request.headers.get('Accept') != '*/*':
        username = request.user.username
        return render(request, 'index.html', {'username': username})
    return render(request, 'stats.html', {'username': username})
    
def tournament(request, username):
    if request.headers.get('Accept') != '*/*':
        return render(request, 'index.html', {'username': username})
    return render(request, 'tournaments.html', {'username': username})


# CRUD API views

@api_view(['POST'])
def createUser(request):
    user = MyCustomUser.objects.filter(username=request.POST.get('username'))
    if user:
        return JsonResponse({'status': 'Username already exists'})
    form = newUser(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': form.errors})
        

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
def get_stats(request, username):
    try:
        user = MyCustomUser.objects.get(username=username)
    except MyCustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    games = Game.objects.filter(Q(player1=user) | Q(player2=user)).select_related('player1', 'player2', 'winner')
    
    #games = Game.objects.filter(player1=user) | Game.objects.filter(player2=user)

    total_conceded = 0
    total_scored = 0
    
    for game in games:

        if game.player1 == user:
            total_scored += game.player1_score
            total_conceded += game.player2_score
        else:
            total_scored += game.player2_score
            total_conceded += game.player1_score 

    games_played = games.count()
    total_possible_points = games_played * 3

    stats_data = {
        'games_played': games_played,
        'total_points': total_possible_points,
        'total_scored': total_scored,
        'total_conceded': total_conceded,
    }

    return JsonResponse(stats_data)

@api_view(['GET'])
def getUserInfo(request):
    if request.user.is_authenticated:
        try:
            user = MyCustomUser.objects.get(username=request.user.username)
            lang = request.user.preferred_language
            context = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'last_login': user.last_login,
                'date_joined': user.date_joined,
                'avatar': user.avatar.url,
                'profile_text': translate('PROFILE', lang),
                'friends_text': translate('FRIENDS', lang),
                'dashboard_text': translate('DASHBOARD', lang),
                'sign_out_text': translate('SIGN_OUT', lang),
            }
            return JsonResponse(context)
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
            'profile_text': 'My profile',
            'friends_text': 'Friends',
            'dashboard_text': 'Dashboard',
            'sign_out_text': 'Sign Out'
        })
        

@api_view(['GET'])
def getUsers(request):
    users = []
    all_users = MyCustomUser.objects.all()
    for user in all_users:
        if not user.is_superuser:
            if user != request.user and user.username != "AI" and user not in request.user.friends.all():
                users.append({'id': user.id, 'username': user.username})
    return JsonResponse(users, safe=False)

@api_view(['GET'])
def getRequests(request, username):
    requests = []
    all_requests = Friend_Request.objects.filter(to_user__username=username)
    for req in all_requests:
        requests.append({'id': req.id, 'from_username': req.from_user.username, 'to_username': req.to_user.username})
    return JsonResponse(requests, safe=False)


@api_view(['GET'])
def getLeaderboards(request):
    users = MyCustomUser.objects.all()
    leaderboard = []
    rank = 1
    for user in users:
        games = Game.objects.filter(player1__username=user.username) | Game.objects.filter(player2__username=user.username)
        gamesWon = games.filter(winner__username=user.username)
        gamesLost = games.exclude(winner__username=user.username)
        goals = 0
        for game in games:
            if game.player1.username == user.username:
                goals += game.player1_score
            else:
                goals += game.player2_score
        score = gamesWon.count() * 10 - gamesLost.count() * 5 + goals
        leaderboard.append({'rank': rank, 'username': user.username, 'score': score})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    for user in leaderboard:
        user['rank'] = rank
        rank += 1
    return JsonResponse(leaderboard, safe=False)

@api_view(['GET'])
def getDashboard(request, username):
    if request.user.is_authenticated and username != 'Guest':
        user = request.user
        games_won = Game.objects.filter(winner=user).count()
        games_lost = Game.objects.filter(Q(player1=user) | Q(player2=user)).exclude(winner=user).count()

        games_details = Game.objects.filter(Q(player1=user) | Q(player2=user)).select_related('player1', 'player2', 'winner')
        games_list = [
            {
                'player1': game.player1.username,
                'player2': game.player2.username,
                'winner': game.winner.username if game.winner else 'None',
                'date': game.date,
                'duration': str(game.duration),
                'player1_score': game.player1_score,
                'player2_score': game.player2_score,
            }
            for game in games_details
        ]

        data = {
            'games_won': games_won,
            'games_lost': games_lost,
            'games_list': games_list,
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Authentication credentials were not provided or username is Guest.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def getFriendList(request, username):
    if (MyCustomUser.objects.filter(username=username).count() == 0):
        return Response({'error': 'User not found'})
    friendlist = []
    order = 1
    user = MyCustomUser.objects.get(username=username)
    friends = user.friends.all()
    for friend in friends:
        friendlist.append({'order': order, 'username': friend.username, 'stat': friend.status})
        order += 1
    return JsonResponse(friendlist, safe=False)

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
    score = gamesWon.count() * 10 - gamesLost.count() * 5 + goals
    return Response({'gamesWon': gamesWon.count(), 'gamesLost': gamesLost.count(), 'goals': goals, 'score': score})

@api_view(['GET'])
def checkwaitlist(request, username):
    response = waiting_room.user_check_if_waiting_is_done(username)
    print(response)
    logger.debug(f" [views] checkwaitlist: {response} ")
    if response is None:
        return JsonResponse({'status': 'waiting'})
    return JsonResponse({'status': 'success', 'response': response})

@api_view(['GET'])
def createGame(request, mode, username):

    if mode.find('AI')>=0:
        m = "AI"
        n = random.randint(100, 99999)
        room_name = "room"+m+str(n)
        status = 'success'
    elif mode.find('vsPlayer')>=0 and mode.find('local')>0:
        m = "PL"
        n = random.randint(100, 99999)
        room_name = "room"+m+str(n)
        status = 'success'
    elif mode.find('vsPlayer')>=0 and mode.find('remote')>0:
        m = "PR"
        waiting_room.add_user(username)
        room_name = 'none'
        status = 'waiting'
    #elif mode.find('tournament')>=0 and mode.find('local')>0:
    #    m = "TL"
    elif mode.find('tournament')>=0 and mode.find('remote')>0:
        m = "TR"
        n = random.randint(100, 99999)
        room_name = "room"+m+str(n)
        status = 'success'
    else:
        m = "error"
        status = 'error'
    return JsonResponse({'status': status, 'room_name': room_name})


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
        user.status = True
        user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid Username or Password', 'username': username})

@api_view(['POST'])
def signOut(request, username):
    user = MyCustomUser.objects.get(username=username)
    user.status = False
    user.save()
    auth.logout(request)
    return JsonResponse({'status': 'success'})

@api_view(['POST'])
def addtowaitlist(request, username):
    logger.debug(f" [views] addtowaitlist: {username} ")
    waiting_room.add_user(username)
    return JsonResponse({'status': 'success'})

@api_view(['POST'])
def send_friend_request(request, userID):
    from_user = request.user
    to_user = MyCustomUser.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
            from_user=from_user, to_user=to_user)
    if created:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

@api_view(['POST'])
def accept_friend_request(request, requestID, accepted):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user and accepted=="accepted":
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return JsonResponse({'status': 'success'})
    else:
        friend_request.delete()
        return JsonResponse({'status': 'error'})

@api_view(['POST'])
def updateProfile(request, username):
    user = MyCustomUser.objects.get(username=username)

    user.username = request.data.get('username')
    user.first_name = request.data.get('first_name')
    user.last_name = request.data.get('last_name')
    user.email = request.data.get('email')
    if not user.save():
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@api_view(['POST'])
def updatePassword(request, username):

    currentPassword = request.data.get('currentPassword')
    newPassword = request.data.get('newPassword')
    confirmPassword = request.data.get('confirmPassword')

    if newPassword == confirmPassword:
        user = MyCustomUser.objects.get(username=username)
        if (user.check_password(currentPassword)):
            user.set_password(newPassword)
            user.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@api_view(['POST'])
def updateAvatar(request, username):
    if request.method == 'POST':
        user = MyCustomUser.objects.get(username=username)
        form = updateAvatarForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
    

# API unused views

@api_view(['GET'])
def getData(request):
    users = MyCustomUser.objects.all()
    serializer = MyCustomUserSerializer(users, many=True)
    return Response(serializer.data)


# Tournament views

@api_view(['POST'])
def add_to_tournament_waiting_room(request, room_id, username):
    logger.debug(f" [views] add_to_tournament_waiting_room: {room_id}, {username} ")
    status = tournament_manager.add_user_to_room(room_id, username)
    return JsonResponse({'status': status})

@api_view(['POST'])
def set_ready_to_play(request, room_id, username):
    logger.debug(f" [views] set_ready_to_play: {room_id}, {username} ")
    status = tournament_manager.user_ready_to_play(room_id, username)
    return JsonResponse({'status': status})

@api_view(['GET'])
def check_tournament_waiting_room(request, room_id):
    logger.debug(f" [views] check_tournament_waiting_room: {room_id} ")
    response = tournament_manager.check_waiting_room(room_id)
    return JsonResponse(response)

@api_view(['GET'])
def get_tournament_game(request, room_id, username):
    logger.debug(f" [views] get_tournament_game: {room_id}, {username} ")
    response = tournament_manager.get_game(room_id, username)
    return JsonResponse(response)

@api_view(['GET'])
def get_tournaments(request, username):
    logger.debug(f" [views] get_tournaments ")
    response = tournament_manager.get_tournaments(username)
    return JsonResponse(response)

@api_view(['GET'])
def get_tournament_state(request, room_id):
    logger.debug(f" [views] get_tournament_state: {room_id} ")
    response = tournament_manager.get_tournament_state(room_id)
    return JsonResponse(response)

@api_view(['GET'])
def stop_game_torunament(request, room_id, winner_id, loser_id):
    logger.debug(f" [views] stop_game: {room_id}, {winner_id}, {loser_id} ")
    tournament_manager.stop_game(room_id, winner_id, loser_id)
    status = 'success'
    return JsonResponse({'status': status})

