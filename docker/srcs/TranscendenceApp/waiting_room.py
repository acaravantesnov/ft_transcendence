from .game import Game

import logging

logger = logging.getLogger("WaitingRoom")

class WaitingRoom:
    def __init__(self):
        # List to store user ids in the waiting room
        self.waiting_users = []

        # Counter to give game rooms unique names
        self.room_counter = 0

        # Self dispatched games
        self.dispatched_games = []

    def add_user(self, user_id):
        logger.debug(f" [WaitingRoom] add_user: {user_id} ")
        self.waiting_users.append(user_id)
        return
    
    def remove_user(self, user_id):
        logger.debug(f" [WaitingRoom] remove_user: {user_id} ")
        self.waiting_users.remove(user_id)
        return

    # When a new game should be created
    # in this case it is when there are 4 users in the waiting room
    def check_waiting_room_condition(self):
        logger.debug(f" [WaitingRoom] check_waiting_room_condition ")
        if len(self.waiting_users) >= 2:
            return True
        return False
    
    # Create a new game room with two random users from the waiting room
    def create_game(self):
        logger.debug(f" [WaitingRoom] create_game ")
        room_name = f"game_{self.room_counter}"
        self.room_counter += 1
        room_name = f"game_{self.room_counter}"
        user_right = self.waiting_users.pop()
        user_left = self.waiting_users.pop()
        self.dispatched_games.append({
            "room_name": room_name,
            "user_left": user_left,
            "user_right": user_right
        })
        return {
            "room_name": room_name,
            "user_left": user_left,
            "user_right": user_right
        }
    
    def user_check_if_waiting_is_done(self, user_id):
        logger.debug(f" [WaitingRoom] user_check_if_waiting_is_done: {user_id} ")
        if self.check_waiting_room_condition():
            self.create_game()
        for game in self.dispatched_games:
            if user_id == game["user_left"] or user_id == game["user_right"]:
                return game
        return None
    
    def remove_game(self, room_name):
        del self.dispatched_games[room_name]


waiting_room = WaitingRoom()
        