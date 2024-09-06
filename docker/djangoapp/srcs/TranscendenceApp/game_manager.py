from .game import Game
from .waiting_room import waiting_room
from .serializers import GameSerializer
from .models import MyCustomUser
from .tournament_manager import tournament_manager
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

    def check_game_exists(self, username):
        try:
            logger.debug(f" [GameManager] check_game_exists: {username} ")
            for room_group_name in self.games:
                logger.debug(f" [GameManager] Checking game {room_group_name} ")
                if self.left_user.get(room_group_name) == username or self.right_user.get(room_group_name) == username:
                    logger.debug(f" [GameManager] Game exists for user {username} , room_group_name: {room_group_name} ")
                    logger.debug(f" [GameManager] left_user: {self.left_user.get(room_group_name)} , right_user: {self.right_user.get(room_group_name)} ")
                    if room_group_name.find("PL")>0: # local game
                        user_left = user_right = username
                    else:
                        user_left = self.left_user[room_group_name]
                        user_right = self.right_user[room_group_name]
                    ret = {
                        "status": "success",
                        "data": {
                            "room_name": room_group_name,
                            "user_left": user_left,
                            "user_right": user_right
                        }
                    }
                    logger.debug(f" [GameManager] Game exists for user {username}: {ret} ")
                    return ret 
                logger.debug(f" [GameManager] Game does not exist for user {username} ")
                return {
                    "status": "error",
                }
        except Exception as e:
            logger.error(f" [GameManager] Error checking if game exists for user {username}: {e} ")
            return {
                "status": f"error: {e}",
            }

    def add_user(self, room_group_name, side, user_id):
        logger.debug(f" [GameManager] add_user: {room_group_name}, {side}, {user_id} ")
        if side == "right":
            self.right_user[room_group_name] = user_id
            self.right_user_connected[room_group_name] = True
            if room_group_name.find("AI")>0:
                self.left_user[room_group_name] = "AI"
                self.left_user_connected[room_group_name] = True
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
        logger.debug(f" [GameManager] remove_user: {room_group_name}, {side}, {user_id} ")
        if side == "left":
            self.left_user_connected[room_group_name] = False
        elif side == "right":
            self.right_user_connected[room_group_name] = False
            if room_group_name.find("AI")>0:
                self.left_user_connected[room_group_name] = False

        # If no users left in the room, stop the game
        if (not self.left_user_connected[room_group_name] and not self.right_user_connected[room_group_name]) or (side == "local"):
            logger.debug(f" [GameManager] No users left in room {room_group_name}, stopping game ")
            #asyncio.create_task(self.stop_game(room_group_name))
            #   await self.stop_game(room_group_name)
            #asyncio.create_task(self.stop_game(room_group_name))
            await self.stop_game(room_group_name, side)
            logger.debug(f" [GameManager] Game stopped ")
            # eg. roomPR73613 is remote game as it has R. eg. roomPL73613 is local game as it has L
            # eg. roomTR73613 is remote tournament as it has T
            # If it is remote game remove from waiting room. If it is local or tournament do not remove from waiting room
            if room_group_name.find("R")>0 and not room_group_name.find("T")>0:
                waiting_room.remove_game(room_group_name)
                logger.debug(f" [GameManager] removed from waiting room: {room_group_name}")
            else:
                logger.debug(f" [GameManager] NOT removed from waiting room: {room_group_name}")

    async def stop_game(self, room_group_name, side):
        try:
            logger.debug(f" [GameManager] stop_game: {room_group_name} ")
            if room_group_name in self.games:
                if side != "local":
                    # Get info of the game before stopping it
                    player1_score = self.games[room_group_name].scores['left']
                    player2_score = self.games[room_group_name].scores['right']
                    winner = self.games[room_group_name].game_over['winner']
                    logger.debug(f" [GameManager] Stopping game for room {room_group_name} ")
                    await self.games[room_group_name].stop()
                    logger.debug(f" [GameManager] Getting players ")
                    player_left_name_str = self.left_user[room_group_name]
                    player_left = await MyCustomUser.get_user_by_username(self.left_user[room_group_name])
                    logger.debug(f" [GameManager] left player: {player_left} ")
                    player_right_name_str = self.right_user[room_group_name]
                    player_right = await MyCustomUser.get_user_by_username(self.right_user[room_group_name])

                    logger.debug(f" [GameManager] right player: {player_right} ")
                    player_winner = player_left if self.games[room_group_name].game_over['winner'] == 'left' else player_right
                    player_winner_name_str = player_left_name_str if self.games[room_group_name].game_over['winner'] == 'left' else player_right_name_str
                    player_loser_name_str = player_left_name_str if self.games[room_group_name].game_over['winner'] == 'right' else player_right_name_str
                    logger.debug(f" [GameManager] winner: {player_winner}, game_over: {winner} ")
                    logger.debug(f" [GameManager] Saving game to database ")
                    game_data = {
                        'player1': player_left.pk,
                        'player2': player_right.pk,
                        'winner': player_winner.pk,
                        'duration': 0,
                        'player1_score': player1_score,
                        'player2_score': player2_score
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
                else:
                    await self.games[room_group_name].stop()
                if self.left_user.get(room_group_name):
                    self.left_user.pop(room_group_name)
                if self.right_user.get(room_group_name):
                    self.right_user.pop(room_group_name)
                if self.left_user_connected.get(room_group_name):
                    self.left_user_connected.pop(room_group_name)
                if self.right_user_connected.get(room_group_name):
                    self.right_user_connected.pop(room_group_name)
                if room_group_name in self.games:
                    self.games.pop(room_group_name)
                    logger.debug(f" [GameManager] Game popped ")
                if room_group_name.find("T")>0:
                    #room_name = 'roomTR52365_level_0_game_0'
                    #torunament_name = 'roomTR52365'
                    logger.debug(f" [GameManager] Removing game {room_group_name}, {room_group_name.find('_level')}")
                    torunament_name = room_group_name[:room_group_name.find('_level')]
                    logger.debug(f" [GameManager] Removing game {room_group_name} in tournament {torunament_name}, player_left: {player_left_name_str}, player_right: {player_right_name_str}")
                    tournament_manager.stop_game(torunament_name, player_winner_name_str, player_loser_name_str)
        except Exception as e:
            logger.error(f" [GameManager] Error stopping game: {e} ")

game_manager = GameManager()
