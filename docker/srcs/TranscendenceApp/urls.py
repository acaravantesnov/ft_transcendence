'''
Maps the view functions to the URL patterns.
'''

from django.urls import path, re_path
from . import views

# URLConf module
urlpatterns = [
    path('', views.title, name="title"),
    path('home/<str:username>', views.home, name="home"),

    path('waitlist/<str:username>/', views.waitlist, name="waitlist"),
    path('play/<str:username>/<str:room_name>/<str:side>/', views.play, name="play"),
    path('leaderboards/<str:username>/', views.leaderboards, name="leaderboards"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('leaderboards/<str:username>', views.leaderboards, name="leaderboards"),
    
    path('getUserInfo/', views.getUserInfo, name="getUserInfo"),

    path('create', views.createUser),
    path('read/<str:pk>', views.readUser),
    path('update/<str:pk>', views.updateUser),
    path('delete/<str:pk>', views.deleteUser),
    path('addGame/', views.addGame),
    path('statistics/<str:username>/', views.statistics, name="statistics"),
    path('checkCredentials/', views.checkCredentials, name="checkCredentials"),
    path('signUp/', views.signUp, name="signUp"),
    path('signUp/createUser/', views.createUser),
    path('signOut/', views.signOut, name="signOut"),
    
    path('waitlist/addtowaitlist/<str:username>/', views.addtowaitlist, name="addtowaitlist"),
    path('waitlist/checkwaitlist/<str:username>/', views.checkwaitlist, name="checkwaitlist"),
]
