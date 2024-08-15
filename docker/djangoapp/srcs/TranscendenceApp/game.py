import asyncio
import json
import logging
import random
import time

from .ai_oponent.config import USERNAME, BUFFER_SIZE
from .ai_oponent.agent import Agent
from .ai_oponent.replay_buffer import ReplayBuffer

logger = logging.getLogger("Game")

class Game:
    def __init__(self, room_group_name, channel_layer):
        logger.debug(f" [Game] __init__: {room_group_name} ")
        self.room_group_name = room_group_name
        self.channel_layer = channel_layer
        self.ball_position = {'x': 400, 'y': 300}
        self.ball_speed = {'x': 4, 'y': 2}
        self.ball_size = {'width': 10, 'height': 10}
        self.screen_size = {'width': 800, 'height': 600}
        self.paddle_size = {'width': 10, 'height': 150}
        self.left_paddle = {'x': 30, 'y': 250, 'speed': 0}
        self.right_paddle = {'x': 760, 'y': 250, 'speed': 0}
        self.scores = {'left': 0, 'right': 0}
        self.game_over = {'ended': False, 'winner': None}
        self.running = False
        self.task = None
        self.duration = time.time()
        if (room_group_name.find("IA")):
            replay_buffer = ReplayBuffer(BUFFER_SIZE)
            self.agent = Agent('right', replay_buffer)

    async def start(self):
        logger.debug(f" [Game] start: {self.room_group_name} ")
        if not self.running:
            logger.debug(f" [Game] Starting game loop ")
            self.running = True
            self.task = asyncio.create_task(self.game_loop())

    async def game_loop(self):
        logger.debug(f" [Game] game_loop: {self.room_group_name} ")
        while self.running:
            self.check_end_game()
            self.update_positions()
            await self.check_collisions()

            # Broadcast game state to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_state',
                    'state': self.get_state()
                }
            )
            await asyncio.sleep(0.03)  # 30 FPS
    
    def check_end_game(self):
        if self.game_over['ended']:
            logger.debug(f" [Game] Returning Game over: {self.game_over['winner']} ")
            #await self.stop()
            print(self.running)
            return True
        if self.scores['left'] >= 3:
            logger.debug(f" [Game] Game over: left ")
            self.game_over = {'ended': True, 'winner': 'left'}
        elif self.scores['right'] >= 3:
            logger.debug(f" [Game] Game over: right ")
            self.game_over = {'ended': True, 'winner': 'right'}
        return False
      

    def update_positions(self):
        self.ball_position['x'] += self.ball_speed['x']
        self.ball_position['y'] += self.ball_speed['y']

        self.left_paddle['y'] += self.left_paddle['speed']
        if (self.room_group_name.find("IA")):
            state = self.get_state()
            print(state)
            self.right_paddle['y'] += self.agent.decide_action(state)

        else:
            self.right_paddle['y'] += self.right_paddle['speed']

        # Keep paddles within the screen
        self.left_paddle['y'] = max(0, min(self.screen_size['height'] - self.paddle_size['height'], self.left_paddle['y']))
        self.right_paddle['y'] = max(0, min(self.screen_size['height'] - self.paddle_size['height'], self.right_paddle['y']))

    async def check_collisions(self):
        # Ball collision with top and bottom
        if self.ball_position['y'] <= 0 or self.ball_position['y'] + self.ball_size['height'] >= self.screen_size['height']:
            self.ball_speed['y'] *= -1

        # Ball collision with paddles
        if self.ball_speed['x'] < 0: # Left paddle
          if self.ball_position['x'] <= self.left_paddle['x'] + self.paddle_size['width'] and self.ball_position['x'] >= self.left_paddle['x']:
              if self.left_paddle['y'] <= self.ball_position['y'] <= self.left_paddle['y'] + self.paddle_size['height']:
                  self.ball_speed['x'] *= -1
                  # Increase speed if paddle is moving in the same direction as the ball and decrease if moving in the opposite direction
                  self.ball_speed['y'] += self.left_paddle['speed'] / 3

        if self.ball_speed['x'] > 0: # Right paddle
          if self.ball_position['x'] + self.ball_size['width'] >= self.right_paddle['x'] and self.ball_position['x'] + self.ball_size['width'] <= self.right_paddle['x'] + self.paddle_size['width']:
              if self.right_paddle['y'] <= self.ball_position['y'] <= self.right_paddle['y'] + self.paddle_size['height']:
                  self.ball_speed['x'] *= -1
                  # Increase speed if paddle is moving in the same direction as the ball and decrease if moving in the opposite direction
                  self.ball_speed['y'] += self.right_paddle['speed'] / 3
                  
        # Used for right paddle when playing against AI so you can't just keep the paddle in the middle
        # if self.ball_position['x'] + self.ball_size['width'] >= self.right_paddle['x'] and self.ball_position['x'] + self.ball_size['width'] <= self.right_paddle['x'] + self.paddle_size['width']:
        #     #if self.right_paddle['y'] <= self.ball_position['y'] <= self.right_paddle['y'] + self.paddle_size['height']:
        #     if random.random() < 0.4:
        #       self.ball_speed['x'] *= -1
        #       # Increase speed if paddle is moving in the same direction as the ball and decrease if moving in the opposite direction
        #       # self.ball_speed['y'] += self.right_paddle['speed'] / 3
        #       # self.ball_speed['y'] += random.choice([-4/3, 4/3, 0, 0])
        #       if self.ball_speed['y'] > 0:
        #         self.ball_speed['y'] += random.choice([0.0, 1.0])
        #       else:
        #         self.ball_speed['y'] -= random.choice([0.0, 1.0])

        
        # Ball out of bounds
        if self.ball_position['x'] <= 0:
            self.scores['right'] += 1
            self.reset_ball('right')
        elif self.ball_position['x'] + self.ball_size['width'] >= self.screen_size['width']:
            self.scores['left'] += 1
            self.reset_ball('left')
        
    def reset_ball(self, last_scored):
        self.ball_position = {'x': self.screen_size['width'] // 2, 'y': self.screen_size['height'] // 2}
        # Speed depends on who scored last and a bit of randomness
        if last_scored == 'left':
            x = -4
        else:
            x = 4
        y = random.choice([-2, 2])
        self.ball_speed = {'x': x, 'y': y}

    async def stop(self):
        logger.debug(f" [Game] stop: {self.room_group_name} ")
        if self.running:
            logger.debug(f" [Game] Stopping game loop ")
            self.running = False
            print("Parando el juego")
            print(self.running)
            logger.debug(f" [Game] Cancelling task ")
            if self.task:
                logger.debug(f" [Game] Cancelling task ")
                self.task.cancel()
                logger.debug(f" [Game] Task cancelled ")
            else:
                logger.debug(f" [Game] Task is None ")
        #self.scores = {'left': 0, 'right': 0}
        self.duration = time.time() - self.duration

    def get_state(self):
        return {
            'ball_position': self.ball_position,
            'ball_speed': self.ball_speed,
            'left_paddle': self.left_paddle,
            'right_paddle': self.right_paddle,
            'scores': self.scores,
            'game_over': self.game_over,
        }

    def update_paddle(self, paddle, speed):
        if paddle == 'left':
            self.left_paddle['speed'] = speed
        elif paddle == 'right':
            self.right_paddle['speed'] = speed
