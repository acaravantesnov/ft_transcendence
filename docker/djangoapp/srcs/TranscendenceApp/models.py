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

'''
What should the MyCustomUser model add to the default User model? (animeflv for the moment)

- avatar: A profile picture for the user.
- rank: The rank of the user.
- friendList: A list of friends that the user has added.
'''
class MyCustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.username

    @classmethod
    async def get_user_by_username(cls, username):
        try:
            return await cls.objects.aget(username=username)
        except cls.DoesNotExist:
            return None

class Game(models.Model):
    player1 = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='player1', null=True)
    player2 = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='player2', null=True)
    winner = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE, related_name='winner', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(default=timezone.timedelta())
    player1_score = models.IntegerField(null=True)
    player2_score = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.player1} vs {self.player2}'
    
    def save(self, *args, **kwargs):
        print(f"Player 1: {self.player1}")
        print(f"Player 2: {self.player2}")
        print(f"Winner: {self.winner}")
        print(f"Date: {self.date}")
        print(f"Duration: {self.duration}")
        print(f"Player 1 Score: {self.player1_score}")
        print(f"Player 2 Score: {self.player2_score}")
        # Ensure that the winner is one of the players or None
        if self.winner not in [self.player1, self.player2, None]:
            raise ValueError("Winner must be either player1, player2, or None.")
        super().save(*args, **kwargs)
