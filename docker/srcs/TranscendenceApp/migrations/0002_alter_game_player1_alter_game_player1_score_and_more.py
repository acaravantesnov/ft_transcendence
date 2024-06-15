# Generated by Django 5.0.6 on 2024-06-11 11:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TranscendenceApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='player1_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='player2_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='mycustomuser',
            name='animeflv',
            field=models.IntegerField(null=True),
        ),
    ]
