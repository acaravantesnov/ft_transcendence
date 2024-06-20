"""
Used to communicate with the websockets.
This is a websocket consumer that listens to the 'game' group and sends the ball position to all the
clients in the group.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game_manager import game_manager
import logging

logger = logging.getLogger("consumers")

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug(f" [GameConsumer] connect: {self.scope} ")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'

        # Join room group
        logger.debug(f" [GameConsumer] Joining room group {self.room_group_name} ")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Get or create game instance
        logger.debug(f" [GameConsumer] Getting game instance for room {self.room_group_name} ")
        self.game = game_manager.get_game(self.room_group_name, self.channel_layer)
        
        # Add user to the room
        logger.debug(f" [GameConsumer] Adding user to room {self.room_group_name} ")
        self.user_number = game_manager.add_user(self.room_group_name)
        logger.debug(f" [GameConsumer] User number: {self.user_number} ")

        # Start the game if not already running
        logger.debug(f" [GameConsumer] Starting game for room {self.room_group_name} ")
        await self.game.start()

        # Send initial game state
        await self.send(text_data=json.dumps({'type': 'game_state', 'state': self.game.get_state()}))

    async def disconnect(self, close_code):
        # Leave room group
        logger.debug(f" [GameConsumer] disconnect: {self.scope} ")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Remove user from the room
        logger.debug(f" [GameConsumer] Removing user from room {self.room_group_name} ")
        game_manager.remove_user(self.room_group_name)

    async def receive(self, text_data):
        logger.debug(f" [GameConsumer] receive: {text_data} ")
        data = json.loads(text_data)
        if data['type'] == 'paddle':
            logger.debug(f" [GameConsumer] Updating paddle for user {self.user_number} ")
            if self.user_number == 1:
                paddle = 'left'
            elif self.user_number == 2:
                paddle = 'right'
            else:
                return
            speed = data['speed']
            self.game.update_paddle(paddle, speed)

    async def game_state(self, event):
        # Called by the game instance to send the game state to the clients
        ended = event['state']['game_over']['ended']
        if ended:
            logger.debug(f" [GameConsumer] Game ended, sending final state ")
            # Save final state in the database
            # ...

        await self.send(text_data=json.dumps({'type': 'game_state', 'state': event['state']}))