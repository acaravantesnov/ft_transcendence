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

from django.contrib.auth.models import AbstractUser

class MyCustomUser(AbstractUser):
    gamesWon = models.IntegerField(default=0)
   # gamesLost = models.IntegerField(default=0)
   # goals = models.IntegerField(default=0)
   # score = models.IntegerField(default=0)

class Game(models.Model):
    player1 = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='player2')
    winner = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='winner', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(default=timezone.timedelta())
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.player1} vs {self.player2}'
    
    def save(self, *args, **kwargs):
        # Ensure that the winner is one of the players or None
        if self.winner not in [self.player1, self.player2, None]:
            raise ValueError("Winner must be either player1, player2, or None.")
        super().save(*args, **kwargs)

