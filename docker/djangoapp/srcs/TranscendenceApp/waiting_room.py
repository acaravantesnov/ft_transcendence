from .game import Game

import random
import logging

logger = logging.getLogger("WaitingRoom")

class WaitingRoom:
    def __init__(self):
        # List to store user ids in the waiting room
        self.waiting_users = []

        # Counter to give game rooms unique names
        self.room_names = []

        # Self dispatched games
        self.dispatched_games = []

    def add_user(self, user_id):
        logger.debug(f" [WaitingRoom] add_user: {user_id} ")
        for waiting_user in self.waiting_users:
            if user_id == waiting_user:
              logger.debug(f" [WaitingRoom] user already in waiting list: {user_id} ")
              return
        self.waiting_users.append(user_id)
        return
    
    def remove_user(self, user_id):
        logger.debug(f" [WaitingRoom] remove_user: {user_id} ")
        self.waiting_users.remove(user_id)
        return

    def add_room(self, room_name):
        logger.debug(f" [WaitingRoom] add_room: {room_name} ")
        self.room_names.append(room_name)
        return

    # When a new gae should be created
    # in this case it is when there are 4 users in the waiting room
    def check_waiting_room_condition(self):
        logger.debug(f" [WaitingRoom] check_waiting_room_condition ")
        print(' [WaitingRoom] room condition')
        if len(self.waiting_users) >= 2:
            self.add_room('roomPR'+str(random.randint(100,99999)))
            return True
        return False
    
    # Create a new game room with two random users from the waiting room
    def create_game(self):
        logger.debug(f" [WaitingRoom] create_game ")
        #room_name = f"game_{self.room_counter}"
        #self.room_counter += 1
        #room_name = f"game_{self.room_counter}"
        print(' [WaitingRoon] creando juego ')
        room_name = self.room_names.pop()
        user_right = self.waiting_users.pop()
        user_left = self.waiting_users.pop()
        self.dispatched_games.append({
            "room_name": room_name,
            "user_left": user_left,
            "user_right": user_right
        })
        logger.debug(f" [WaitingRoom] self.dispatched_games: {self.dispatched_games}")
        return {
            "room_name": room_name,
            "user_left": user_left,
            "user_right": user_right
        }
    
    def user_check_if_waiting_is_done(self, user_id):
        logger.debug(f" [WaitingRoom] self.waaaiting_users: {self.waiting_users}")
        logger.debug(f" [WaitingRoom] user_check_if_waiting_is_done: {user_id} ")
        print(' [WaitingRoom] user_check ')
        if self.check_waiting_room_condition():
            self.create_game()
        for game in self.dispatched_games:
            print(' [WaitingRoom] Comprobando dispatched_games ')
            if user_id == game["user_left"] or user_id == game["user_right"]:
                print(' [WaitingRoom] Dispatched_game encontrado ')
                return game
        return None
    
    def remove_game(self, room_name):
        logger.debug(f" [WaitingRoom] removing game: {room_name}")
        logger.debug(f" [WaitingRoom] self.dispatched_games: {self.dispatched_games}")
        for dispatched_game in self.dispatched_games:
          if dispatched_game["room_name"] == room_name:
            self.dispatched_games.remove(dispatched_game)
            logger.debug(f" [WaitingRoom] Game {room_name} removed")
            break
        else:
          logger.debug(f" [WaitingRoom] Game {room_name} not found")




waiting_room = WaitingRoom()
        
