'''
Maps the view functions to the URL patterns.
'''

from django.urls import path, re_path
from . import views

# URLConf module
urlpatterns = [
    # Normal views
    path('', views.title, name="title"),
    path('home/<str:username>', views.home, name="home"),
    path('play/<str:username>/', views.play, name="play"),
    path('leaderboards/<str:username>/', views.leaderboards, name="leaderboards"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('profile/<str:username>/friends', views.profile, name="friends"),
    path('signUp/', views.signUp, name="signUp"),

    # CRUD API views
    path('create', views.createUser), # API POST
    path('read/<str:pk>', views.readUser), # API GET
    path('update/<str:pk>', views.updateUser), # API PUT
    path('delete/<str:pk>', views.deleteUser), # API DELETE
    
    # API GET views
    path('getUserInfo/', views.getUserInfo, name="getUserInfo"),
    path('getLeaderboards/', views.getLeaderboards, name="getLeaderboards"),
    path('statistics/<str:username>/', views.statistics, name="statistics"),
    path('waitlist/checkwaitlist/<str:username>/', views.checkwaitlist, name="checkwaitlist"),
    
    # API POST views
    path('checkCredentials/', views.checkCredentials, name="checkCredentials"),
    path('signUp/createUser/', views.createUser),
    path('signOut/', views.signOut, name="signOut"),
    path('waitlist/addtowaitlist/<str:username>/', views.addtowaitlist, name="addtowaitlist"),
]
