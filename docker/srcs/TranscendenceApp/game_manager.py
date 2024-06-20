from .game import Game

import logging

logger = logging.getLogger("GameManager")



class GameManager:
    def __init__(self):
        # Dictionary to store game instances
        self.games = {}
        # Dictionary to store user counts for each room (I think it should be user ids in the future)
        self.user_counts = {}

    def get_game(self, room_group_name, channel_layer):
        logger.debug(f" [GameManager] get_game: {room_group_name} ")
        if room_group_name not in self.games:
            logger.debug(f" [GameManager] Creating new game for room {room_group_name} ")
            self.games[room_group_name] = Game(room_group_name, channel_layer)
            self.user_counts[room_group_name] = 0
        return self.games[room_group_name]

    def add_user(self, room_group_name):
        logger.debug(f" [GameManager] add_user: {room_group_name} ")
        if room_group_name in self.user_counts:
            logger.debug(f" [GameManager] Adding user to room {room_group_name} ")
            self.user_counts[room_group_name] += 1
            return self.user_counts[room_group_name]
        logger.debug(f" [GameManager] Room {room_group_name} not found ")
        return 1

    def remove_user(self, room_group_name):
        logger.debug(f" [GameManager] remove_user: {room_group_name} ")
        if room_group_name in self.user_counts:
            logger.debug(f" [GameManager] Removing user from room {room_group_name} ")
            self.user_counts[room_group_name] -= 1
            if self.user_counts[room_group_name] <= 0:
                logger.debug(f" [GameManager] No users left in room {room_group_name}, stopping game ")
                asyncio.create_task(self.stop_game(room_group_name))
                logger.debug(f" [GameManager] Game stopped ")

    async def stop_game(self, room_group_name):
        logger.debug(f" [GameManager] stop_game: {room_group_name} ")
        if room_group_name in self.games:
            logger.debug(f" [GameManager] Stopping game for room {room_group_name} ")
            await self.games[room_group_name].stop()
            del self.games[room_group_name]
            del self.user_counts[room_group_name]
            logger.debug(f" [GameManager] Game stopped ")

game_manager = GameManager()