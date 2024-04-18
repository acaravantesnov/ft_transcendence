from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path ('create', views.addUser),
    path ('read/<str:pk>', views.getUser),
    path ('update/<str:pk>', views.updateUser),
    path ('delete/<str:pk>', views.deleteUser),
    path('sign/', views.signIn, name="sign"),
    path('signUp/', views.signUp, name="signUp"),
    path('signed/<str:username>', views.signed, name="signed"),
    path('logout', views.logOut, name="logout")
]
