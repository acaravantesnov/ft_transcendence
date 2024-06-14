'''
Maps the view functions to the URL patterns.
'''

from django.urls import path, re_path
from . import views

# URLConf module
urlpatterns = [
    path('', views.getData),
    path('create', views.addUser),
    path('addGame', views.addGame),
    path('read/<str:pk>', views.getUser),
    path('update/<str:pk>', views.updateUser),
    path('delete/<str:pk>', views.deleteUser),
    path('signIn/', views.signIn, name="signIn"),
    path('signUp/', views.signUp, name="signUp"),
    path('signed/<str:username>', views.home, name="signed"),
    path('signOut/', views.signOut, name="signout"),
    path('statistics/gamesWon/<str:username>', views.getGamesWon, name="statistics1"),
    path('statistics/gamesLost/<str:username>', views.getGamesLost, name="statistics2"),
    path('statistics/goals/<str:username>', views.getGoals, name="statistics3"),
    path('game', views.game, name='game'),
    # path('game2', views.game2, name='game2'),
    # re_path(r'^game2/(?P<room_name>\w+)/$', views.game2, name='game2'),
    path('game2/<str:room_name>/', views.game2, name='game2'),
]
