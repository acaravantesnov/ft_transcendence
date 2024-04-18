from django.db import models
from django.utils import timezone

#-----------------------------------------------------------------
from django.contrib.auth.models import User

class MyCustomUser(User):
    animeflv = models.CharField(max_length = 25)


#-----------------------------------------------------------------


# Create your models here.
#class User(models.Model):
#    username = models.CharField(max_length = 25, unique=True)
#    password = models.CharField(max_length = 25)
#
#class Core(models.Model):
#    username = models.CharField(max_length=25, unique=True)
#    firstname = models.CharField(max_length=15)
#    lastname = models.CharField(max_length=15)
#    email = models.EmailField()
#    password = models.CharField(max_length=12)
#    passwordR = models.CharField(max_length=12)
