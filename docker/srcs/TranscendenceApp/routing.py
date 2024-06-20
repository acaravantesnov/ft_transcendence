"""
Used to communicate with the websockets
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game2/(?P<room_name>\w+)/$', consumers.GameConsumer.as_asgi()),
]