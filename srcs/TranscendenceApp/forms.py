from django.contrib.auth.models import User
from django import forms
from .models import Core
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib.auth import authenticate, login

class signUser(forms.Form):
    
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput,label="password")
   
    def validate(self):
        username = self['username'].value()
        password = self['password'].value()
 
        print(Core.objects)
        username_qs = Core.objects.filter(username=username)
        #if not username_qs.exists():
            #raise forms.ValidationError("Username does not exists")
        #print(username_qs[0])
        #if username_qs['password'].value() != password:
            #raise forms.ValidationError("Wrong Password")
        return username

    
class newUser(forms.ModelForm):
    username = forms.CharField(max_length=15, label="Username")
    firstname = forms.CharField(max_length=15, label="Firstname")
    lastname = forms.CharField(max_length=15, label="Lastname")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    passwordR = forms.CharField(widget=forms.PasswordInput,label="Repeat password")

    class Meta:
        model = Core
        fields = ("username", "firstname", "lastname", "email", "password", "passwordR")

    def validate_username(self):
        username = self.data['username']
        username_qs = Core.objects.filter(username=username)
        #if username_qs.exists():
          #  raise ValidationError("Username already exists")
        return username

    def validate_password(self):
        password = self.data['password']
        passwordR = self.data['passwordR']
        #if password and passwordR and password != passwordR:
           # raise ValidationError("Password didn't match")
        return password
