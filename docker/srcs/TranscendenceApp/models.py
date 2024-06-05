'''
Defines the model classes for this app.
Model classes are used to pull out data from the database and present it
to the user.

Django uses an ORM (Object Relational Mapping) to map a python object to a database table. This
allows to use multiple types of databases and have django handle all the low-level commands that
actually create, update and retrieve data.
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

    def __str__(self):
        return f'{self.player1} vs {self.player2}'
