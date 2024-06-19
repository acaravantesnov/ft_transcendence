'''
Maps the view functions to the URL patterns.
'''

from django.urls import path, re_path
from . import views

# URLConf module
urlpatterns = [
    path('', views.title, name="title"),
    path('home/<str:username>', views.home, name="home"),
    path('getCurrentUsername/', views.getCurrentUsername, name="getCurrentUsername"),
    path('create', views.createUser),
    path('read/<str:pk>', views.readUser),
    path('update/<str:pk>', views.updateUser),
    path('delete/<str:pk>', views.deleteUser),
    path('addGame/', views.addGame),
    path('statistics/<str:username>', views.statistics, name="statistics"),
    path('checkCredentials/', views.checkCredentials, name="checkCredentials"),
    path('signUp/', views.signUp, name="signUp"),
    path('signUp/createUser/', views.createUser),
    path('signOut/', views.signOut, name="signOut"),
    path('game/<str:username>', views.game, name="game"),
]
