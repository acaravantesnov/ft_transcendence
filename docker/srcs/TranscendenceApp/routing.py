"""
Used to communicate with the websockets
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.side = self.scope['url_route']['kwargs']['side']
        # self.user_id = self.scope['url_route']['kwargs']['user_id']
    # const socket = new WebSocket('ws://' + window.location.host + '/ws/game2/digarcia/' + roomName + '/left/');
    re_path(r'ws/game2/(?P<user_id>\w+)/(?P<room_name>\w+)/(?P<side>\w+)/$', consumers.GameConsumer.as_asgi()),
]