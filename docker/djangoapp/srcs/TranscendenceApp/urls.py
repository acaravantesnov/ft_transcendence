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
    path('friends/<str:username>/', views.friends, name="friends"),
    path('signUp/', views.signUp, name="signUp"),
    path('editProfile/', views.editProfile, name="editProfile"),
    path('changePassword/', views.changePassword, name="newPassword"),

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
    path('statistics/<str:username>/', views.statistics, name="statistics"),
    path('waitlist/checkwaitlist/<str:username>/', views.checkwaitlist, name="checkwaitlist"),
    
    # API POST views
    path('checkCredentials/', views.checkCredentials, name="checkCredentials"),
    path('signUp/createUser/', views.createUser),
    path('signOut/<str:username>/', views.signOut, name="signOut"),
    path('waitlist/addtowaitlist/<str:username>/', views.addtowaitlist, name="addtowaitlist"),
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID><str:accepted>/', views.accept_friend_request, name='accept_friend_request'),
    path('editProfile/upadateProfile/<str:username>/', views.editProfile),
    path('changePassword/upadatePassword/<str:username>/', views.changePassword),

]
