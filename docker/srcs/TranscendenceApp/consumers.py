"""
Used to communicate with the websockets.
This is a websocket consumer that listens to the 'game' group and sends the ball position to all the
clients in the group.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import asyncio
import aioredis
import logging

logger = logging.getLogger("game")

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'
        logger.debug(f'room_group_name: {self.room_group_name}')

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Connect to Redis
        self.redis = await aioredis.create_redis_pool('redis://localhost')

        # Get or set initial ball position
        # TODO: It is not the best way to check if it is the first player as if you exit there will be a ball position saved, but noone running the game loop
        ball_position = await self.get_ball_position()
        if ball_position is None:
            ball_position = {'x': 50, 'y': 50}
            await self.set_ball_position(ball_position)
            logger.debug(f'Started ball position for room {self.room_name} at {ball_position}')
            is_first_player = True
        else:
            is_first_player = False  

        # Send initial ball position
        await self.send(text_data=json.dumps(ball_position))

        # Start the game loop
        if is_first_player:
          logger.debug('Starting game_loop')
          self.game_task = asyncio.create_task(self.game_loop())
          logger.debug('Started game_loop')

    async def disconnect(self, close_code):
        logger.debug(f'Disconnecting from {self.room_name}')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Cancel the game loop
        # TODO: maybe it should check if there is still some people
        self.game_task.cancel()

        # Close Redis connection
        self.redis.close()
        await self.redis.wait_closed()

    async def receive(self, text_data):
        pass  # No need to handle client messages in this example

    async def game_loop(self):
      try:
        logger.debug(f'Started game_loop {self.room_name}')
        ball_position = await self.get_ball_position()
        ball_speed = {'x': 2, 'y': 2}
        # ball_speed = {'x': 20, 'y': 20}
        ball_size = {'width': 50, 'height': 50}
        screen_size = {'width': 800, 'height': 600}  # fixed size for all users

        while True:
            ball_position['x'] += ball_speed['x']
            ball_position['y'] += ball_speed['y']

            if (ball_position['x'] + ball_size['width'] >= screen_size['width'] or ball_position['x'] <= 0):
                ball_speed['x'] *= -1

            if (ball_position['y'] + ball_size['height'] >= screen_size['height'] or ball_position['y'] <= 0):
                ball_speed['y'] *= -1

            # Update ball position in Redis
            await self.set_ball_position(ball_position)
            logger.debug(f'Possition: {ball_position}')

            # Broadcast ball position to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ball_position',
                    'position': ball_position
                }
            )
            logger.debug('Possition Shared')

            await asyncio.sleep(0.03)  # 30 FPS
            # await asyncio.sleep(1.0)  # 1 FPS
      except asyncio.CancelledError:
        logger.info('Game loop cancelled')
      except Exception as e:
        logger.error(f'Error in game_loop: {e}')


    async def ball_position(self, event):
        await self.send(text_data=json.dumps(event['position']))

    async def get_ball_position(self):
        ball_position = await self.redis.get(f'{self.room_group_name}_ball_position')
        logger.debug(f'get_ball_position: {ball_position}')
        if ball_position:
            return json.loads(ball_position)
        return None

    async def set_ball_position(self, position):
        logger.debug(f'set_ball_position: {position}')
        await self.redis.set(f'{self.room_group_name}_ball_position', json.dumps(position))
