'''
Enables the conversion of complex data types to native Python datatypes that can then be easily
rendered into JSON, XML or other content types.
'''

from rest_framework import serializers
from .models import MyCustomUser, Game

class MyCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCustomUser
        fields = '__all__'
        
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'