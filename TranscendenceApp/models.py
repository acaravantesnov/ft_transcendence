from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 250)
    email = models.CharField(max_length = 250)

class Test(models.Model):
    name = models.CharField(max_length = 250)
    lm = models.CharField(max_length = 250)