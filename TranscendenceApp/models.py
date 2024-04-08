from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 250)
    email = models.CharField(max_length = 250)


class Game(models.Model):
    # Choices for game status
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    GAME_STATUS_CHOICES = [
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed'),
    ]

    # Player 1 and Player 2 fields as foreign keys to the User model
    player1 = models.ForeignKey(User, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2', on_delete=models.CASCADE)

    # Fields to store player scores
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()

    # Field to store game status
    game_status = models.CharField(max_length=50, choices=GAME_STATUS_CHOICES, default=ONGOING)

    # Field to store the time the game started
    time_started = models.DateTimeField(default=timezone.now)

    # Field to store the time the game ended
    time_ended = models.DateTimeField(null=True, blank=True)

    def end_game(self):
        """
        Method to end the game and update game status and end time.
        """
        self.game_status = self.COMPLETED
        self.time_ended = timezone.now()
        self.save()