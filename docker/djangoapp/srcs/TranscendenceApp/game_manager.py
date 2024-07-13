from .game import Game
from .waiting_room import waiting_room
from .serializers import GameSerializer
from .models import MyCustomUser
from asgiref.sync import sync_to_async

import logging

logger = logging.getLogger("GameManager")

class GameManager:
    def __init__(self):
        # Dictionary to store game instances
        self.games = {}
        # Dictionary to store user counts for each room (I think it should be user ids in the future)
        # self.user_counts = {}

        #Dictionary to save what user is on the left
        self.left_user = {}
        #Dictionary to save what user is on the right
        self.right_user = {}

        self.left_user_connected = {}
        self.right_user_connected = {}

    def get_game(self, room_group_name, channel_layer):
        logger.debug(f" [GameManager] get_game: {room_group_name} ")
        if room_group_name not in self.games:
            logger.debug(f" [GameManager] Creating new game for room {room_group_name} ")
            self.games[room_group_name] = Game(room_group_name, channel_layer)
            # self.user_counts[room_group_name] = 0
        return self.games[room_group_name]

    def add_user(self, room_group_name, side, user_id):
        logger.debug(f" [GameManager] add_user: {room_group_name}, {side}, {user_id} ")
        if side == "right":
            self.right_user[room_group_name] = user_id
            self.right_user_connected[room_group_name] = True
            return 0
        elif side == "left":
            self.left_user[room_group_name] = user_id
            self.left_user_connected[room_group_name] = True
            return 0
        logger.debug(f" [GameManager] User not added to room {room_group_name} ")
        return 1

    async def remove_user(self, room_group_name, side, user_id):
    #     logger.debug(f" [GameManager] remove_user: {room_group_name} ")
    #     if room_group_name in self.user_counts:
    #         logger.debug(f" [GameManager] Removing user from room {room_group_name} ")
    #         self.user_counts[room_group_name] -= 1
    #         if self.user_counts[room_group_name] <= 0:
    #             logger.debug(f" [GameManager] No users left in room {room_group_name}, stopping game ")
    #             asyncio.create_task(self.stop_game(room_group_name))
    #             logger.debug(f" [GameManager] Game stopped ")
          logger.debug(f" [GameManager] remove_user: {room_group_name} ")
          if side == "left":
              self.left_user_connected[room_group_name] = False
          elif side == "right":
              self.right_user_connected[room_group_name] = False

          # If no users left in the room, stop the game
          if not self.left_user_connected[room_group_name] and not self.right_user_connected[room_group_name]:
              logger.debug(f" [GameManager] No users left in room {room_group_name}, stopping game ")
              #asyncio.create_task(self.stop_game(room_group_name))
              #   await self.stop_game(room_group_name)
              #asyncio.create_task(self.stop_game(room_group_name))
              await self.stop_game(room_group_name)
              logger.debug(f" [GameManager] Game stopped ")
              waiting_room.delete_game(room_group_name)


    async def stop_game(self, room_group_name):
        try:
            logger.debug(f" [GameManager] stop_game: {room_group_name} ")
            if room_group_name in self.games:
                logger.debug(f" [GameManager] Stopping game for room {room_group_name} ")
                await self.games[room_group_name].stop()
                logger.debug(f" [GameManager] Getting players ")
                player_left = await MyCustomUser.get_user_by_username(self.left_user[room_group_name])
                logger.debug(f" [GameManager] left player: {player_left} ")
                player_right = await MyCustomUser.get_user_by_username(self.right_user[room_group_name])
                logger.debug(f" [GameManager] right player: {player_right} ")
                player_winner = player_left if self.games[room_group_name].game_over['winner'] == 'left' else player_right
                logger.debug(f" [GameManager] winner: {player_winner}, game_over: {self.games[room_group_name].game_over['winner']} ")
                logger.debug(f" [GameManager] Saving game to database ")
                game_data = {
                    'player1': player_left.pk,
                    'player2': player_right.pk,
                    'winner': player_winner.pk,
                    'duration': 0,
                    'player1_score': self.games[room_group_name].scores['left'],
                    'player2_score': self.games[room_group_name].scores['right']
                }
                logger.debug(f" [GameManager] Game data: {game_data} ")
                try:
                    # The problem was that the serializer has to run in a sync function and we are 
                    # in an async function. This is why we have to use sync_to_async
                    serializer = GameSerializer(data=game_data)
                    logger.debug(f" [GameManager] Game data: {serializer} ")
                    is_valid = await sync_to_async(serializer.is_valid)()
                    if is_valid:
                        logger.debug(f" [GameManager] Game data valid ")
                        await sync_to_async(serializer.save)()
                        logger.debug(f" [GameManager] Game saved ")
                    else:
                        logger.error(f" [GameManager] Error saving game to database: {serializer.errors} ")
                except Exception as e:
                    logger.error(f" [GameManager] Catched Error saving game to database: {e} ")
                logger.debug(f" [GameManager] Deleting game instance")
                del self.left_user[room_group_name]
                del self.right_user[room_group_name]
                del self.left_user_connected[room_group_name]
                del self.right_user_connected[room_group_name]
                del self.games[room_group_name]
                logger.debug(f" [GameManager] Game stopped ")
        except Exception as e:
            logger.error(f" [GameManager] Error stopping game: {e} ")

game_manager = GameManager()