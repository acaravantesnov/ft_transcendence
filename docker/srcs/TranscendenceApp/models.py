'''
Defines the model classes for this app.
Model classes are used to pull out data from the database and present it
to the user.
'''

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class MyCustomUser(User):
    animeflv = models.CharField(max_length = 25)

class Game(models.Model):
    player1 = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='player2')
    winner = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='winner')
    date = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField()
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()
