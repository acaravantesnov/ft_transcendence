'''
Maps the view functions to the URL patterns.
'''

from django.urls import path, re_path, include
from . import views

# URLConf module
urlpatterns = [
    # Normal views
    path('', views.title, name="title"),
    path('home/<str:username>', views.home, name="home"),
    path('play/<str:username>/', views.menu, name="menu"),
    path('play/mode/<str:mode>/<str:username>/', views.modeMenu, name="modeMenu"),
    path('play/tournament/<str:username>', views.tournament, name="tournament"),
    path('playing/<str:username>/', views.playing, name="playing"),
    path('play/checkGameExists/<str:username>/', views.check_game_exists, name="check_game_exists"),
    #path('play/<str:username>/', views.play, name="play"),
    path('leaderboards/<str:username>/', views.leaderboards, name="leaderboards"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('friends/<str:username>/', views.friends, name="friends"),
    path('signUp/', views.signUp, name="signUp"),
    path('dashboard/<str:username>/', views.dashboard, name="dashboard"),
    path('editProfile/', views.editProfile, name="editProfile"),
    path('changePassword/', views.changePassword, name="changePassword"),
    path('stats/<str:username>/', views.stats, name='stats'),
    path('getStats/<str:username>/', views.get_stats, name='get_stats'),
    path('changePassword/', views.changePassword, name="changePassword"),
    path('change_language/<str:lang>/', views.change_language, name='change_language'),
    
    # CRUD API views
    path('create', views.createUser), # API POST
    path('read/<str:pk>', views.readUser), # API GET
    path('update/<str:pk>', views.updateUser), # API PUT
    path('delete/<str:pk>', views.deleteUser), # API DELETE
    
    # API GET views
    path('getUserInfo/', views.getUserInfo, name="getUserInfo"),
    path('getUsers/', views.getUsers, name="getUsers"),
    path('getRequests/<str:username>', views.getRequests, name="getRequests"),
    path('getFriendList/<str:username>', views.getFriendList, name="getFriendList"),
    path('getLeaderboards/', views.getLeaderboards, name="getLeaderboards"),
    path('getDashboard/<str:username>/', views.getDashboard, name="getDashboard"),
    path('statistics/<str:username>/', views.statistics, name="statistics"),
    path('waitlist/checkwaitlist/<str:username>/', views.checkwaitlist, name="checkwaitlist"),
    path('play/createGame/<str:mode>/<str:username>/', views.createGame, name="createGame"),
    
    # API POST views
    path('checkCredentials/', views.checkCredentials, name="checkCredentials"),
    path('signUp/createUser/', views.createUser),
    path('signOut/<str:username>/', views.signOut, name="signOut"),
    path('waitlist/addtowaitlist/<str:username>/', views.addtowaitlist, name="addtowaitlist"),
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID><str:accepted>/', views.accept_friend_request, name='accept_friend_request'),
    path('editProfile/updateProfile/<str:username>/', views.updateProfile),
    path('changePassword/updatePassword/<str:username>/', views.updatePassword),
    path('updateAvatar/<str:username>/', views.updateAvatar),

    # Tournament views
    path('tournament/addtowaitingroom/<str:room_id>/<str:username>/', views.add_to_tournament_waiting_room, name='add_to_tournament_waiting_room'),
    path('tournament/checkwaitingroom/<str:room_id>/', views.check_tournament_waiting_room, name='check_tournament_waiting_room'),
    path('tournament/readytoplay/<str:room_id>/<str:username>/', views.set_ready_to_play, name='ready_to_play'),
    path('tournament/getgame/<str:room_id>/<str:username>/', views.get_tournament_game, name='get_tournament_game'),
    path('tournament/gettournaments/<str:username>/', views.get_tournaments, name='get_tournaments'),
    path('tournament/getstate/<str:room_id>/', views.get_tournament_state, name='get_tournament_state'),
    path('tournament/stopgame/<str:room_id>/<str:winner_id>/<str:loser_id>/', views.stop_game_torunament, name='stop_game'),
]

