import logging
from collections import defaultdict, deque
from .game import Game
from .models import MyCustomUser
from asgiref.sync import sync_to_async

logger = logging.getLogger("TournamentManager")

class TournamentManager:
    def __init__(self):
        # Store tournament trees by room_id
        self.tournaments = defaultdict(lambda: defaultdict(lambda: defaultdict(dict))) # room_id -> level -> game_id -> game_info [status,room_name,left_user, right_user]
        self.active_games = defaultdict(dict)  # room_id -> user_id -> (level, game_id)
        self.ready_users = defaultdict(set)  # room_id -> set of users ready to play
        self.waiting_users = defaultdict(list)  # room_id -> users waiting for the next round
        self.status = defaultdict(str)  # room_id -> status of the tournament

    def add_user_to_room(self, room_id, user_id):
        print('Adding user')
        if self.status[room_id] in ["ready", "finished"]:
            print('Tournament already started')
            logger.debug(f" [TournamentManager] Tournament in room {room_id} has already started")
            return "error: tournament already started"

        if room_id not in self.waiting_users:
            print('Addng to waiters')
            # If room does not exist a waiting room for it is added
            self.waiting_users[room_id]
            print('Added to waiters')
            logger.debug(f" [TournamentManager] Tournament room added")

        if user_id in self.waiting_users[room_id]:
            print('Already in waiters')
            logger.debug(f" [TournamentManager] User {user_id} already in waiting list in room {room_id}")
            return "error: already in waiting list"

        self.waiting_users[room_id].append(user_id)
        logger.debug(f" [TournamentManager] Added user {user_id} to waiting list in room {room_id}")

        return "success"
        

    def _initialize_tournament(self, room_id, n_users):
        # Initialize the tournament tree with empty placeholders for games
        # We assume a power of 2 for the number of players (e.g., 4, 8, 16)
        logger.debug(f" [TournamentManager] Initializing tournament tree for room {room_id}")
        number_of_games = 1  # Start with a single game
        level = 0
        number_of_games_upperbound = n_users // 2
        while number_of_games <= number_of_games_upperbound:  # Adjust this limit for larger tournaments
            for game_id in range(number_of_games):
                logger.debug(f" [TournamentManager] Adding game {game_id} at level {level}")
                self.tournaments[room_id][level][game_id] = {"status": "waiting", "user_left": None, "user_right": None}
            logger.debug(f" [TournamentManager] Added {number_of_games} games at level {level}")
            number_of_games *= 2
            level += 1
        logger.debug(f" [TournamentManager] Initialized tournament tree for room {room_id}")
        logger.debug(f" [TournamentManager] Full tree: {self.tournaments[room_id]}")

        #Fill the first round of games
        for i in range(n_users//2):
            if n_users == 2:
                level = 0
            elif n_users == 4:
                level = 1
            elif n_users == 8:
                level = 2
            elif n_users == 16:
                level = 3
            self._create_game(room_id, level, user_left=self.waiting_users[room_id][0], user_right=self.waiting_users[room_id][1], game_id=i)
            self.waiting_users[room_id].pop(0)
            self.waiting_users[room_id].pop(0)

        logger.debug(f" [TournamentManager] Filled first round of games for room {room_id}")
        logger.debug(f" [TournamentManager] Full tree: {self.tournaments[room_id]}")

    def _create_game(self, room_id, level, user_left, user_right, game_id):
        # user_left = self.waiting_users[room_id].pop(0)
        # user_right = self.waiting_users[room_id].pop(0)
        logger.debug(f" [TournamentManager] Creating game at level {level} in room {room_id}")
        logger.debug(f" [TournamentManager] Game ID: {game_id}")
        room_name = f"{room_id}_level_{level}_game_{game_id}"
        logger.debug(f" [TournamentManager] Room name: {room_name}")

        game = {
            "status": "playing",
            "room_name": room_name,
            "user_left": user_left,
            "user_right": user_right
        }

        self.tournaments[room_id][level][game_id] = game
        self.active_games[room_id][user_left] = (level, game_id)
        self.active_games[room_id][user_right] = (level, game_id)
        logger.debug(f" [TournamentManager] Created game {game_id} at level {level} in room {room_id}")

    def user_ready_to_play(self, room_id, user_id):
        if user_id in self.ready_users[room_id]:
            logger.debug(f" [TournamentManager] User {user_id} already ready to play")
            return "error"

        if user_id not in self.waiting_users[room_id]:
            logger.debug(f" [TournamentManager] User {user_id} not in waiting list in room {room_id}")
            return "error"

        if self.status[room_id] in ["ready", "finished"]:
            logger.debug(f" [TournamentManager] Tournament in room {room_id} has already started")
            return "error"


        self.ready_users[room_id].add(user_id)
        logger.debug(f" [TournamentManager] User {user_id} marked as ready to play in room {room_id}")
        return "success"

    def check_waiting_room(self, room_id):
        users_waiting = self.waiting_users[room_id]
        response = [
            {"user_id": user_id, "ready_to_play": user_id in self.ready_users[room_id]}
            for user_id in users_waiting
        ]
        logger.debug(f" [TournamentManager] response: {response}")
        logger.debug(f" [TournamentManager] Status: {self.status[room_id]}")
        if self.status[room_id] == "ready":
            logger.debug(f" [TournamentManager] Tournament in room {room_id} is ready to start")
            return {"status": self.status[room_id], "people waiting": response}
        print('Room')
        print(room_id)
        print('Waiting users...')
        print(len(users_waiting))
        print('Ready users...')
        print(len(self.ready_users[room_id]))
        if len(users_waiting) == len(self.ready_users[room_id]) and (len(users_waiting) == 2 or len(users_waiting) == 4 or len(users_waiting) == 8 or len(users_waiting) == 16):
            # Start the torunament
            logger.debug(f" [TournamentManager] Starting tournament in room {room_id}")
            self._initialize_tournament(room_id, len(users_waiting))
            self.status[room_id] = "ready"
            return {"status": self.status[room_id], "people waiting": response}
        else:
            self.status[room_id] = "waiting"
            logger.debug(f" [TournamentManager] Tournament in room {room_id} is not ready to start")
            return {"status": self.status[room_id], "people waiting": response}

    def get_game(self, room_id, user_id):
        if user_id not in self.active_games[room_id]:
            logger.debug(f" [TournamentManager] User {user_id} is not in an active game in room {room_id}")
            return {"status": "error"}

        level, game_id = self.active_games[room_id][user_id]
        logger.debug(f" [TournamentManager] User {user_id} is in game {game_id} at level {level} in room {room_id}")
        game = self.tournaments[room_id][level][game_id]
        logger.debug(f" [TournamentManager] Game state: {game}")

        if game['status'] == 'playing':
            return {
                "status": "success",
                "response": {
                    "room_name": game['room_name'],
                    "user_left": game['user_left'],
                    "user_right": game['user_right']
                }
            }
          
        logger.debug(f" [TournamentManager] User {user_id} is not in an active game in room {room_id}")

        return {"status": "wait"}

    def get_tournament_state(self, room_id):
        if self.status[room_id] not in ["ready", "finished"]:
            logger.debug(f" [TournamentManager] Tournament in room {room_id} is not ready")
            return {
                "status": "error",
                "message": "Tournament not ready"
            }
        logger.debug(f" [TournamentManager] Getting tournament state for room {room_id}")
        levels = self.tournaments[room_id]
        logger.debug(f" [TournamentManager] Levels: {levels}")
        tournament_state = {
            level: {
                game_id: game
                for game_id, game in games.items()
            }
            for level, games in levels.items()
        }
        logger.debug(f" [TournamentManager] Tournament state for room {room_id}: {tournament_state}")
        return {
            "status": "success",
            "tournament": tournament_state
        }

    def stop_game(self, room_id, winner_id, loser_id):
        logger.debug(f" [TournamentManager] Stopping game for room {room_id}")
        level, game_id = self.active_games[room_id][winner_id]
        logger.debug(f" [TournamentManager] Stopping game {game_id} in room {room_id} at level {level}")
        game = self.tournaments[room_id][level][game_id]
        game['status'] = 'finished'
        game['winner'] = winner_id
        game['loser'] = loser_id

        logger.debug(f" [TournamentManager] Stopped game {game_id} in room {room_id} at level {level}")

        del self.active_games[room_id][winner_id]
        del self.active_games[room_id][loser_id]

        logger.debug(f" [TournamentManager] Removed users {winner_id} and {loser_id} from active games in room {room_id}")

        # Advance the winner to the next level
        next_level = level - 1
        logger.debug(f" [TournamentManager] next_level: {next_level}")
        logger.debug(f" [TournamentManager] game_id % 2: {game_id % 2}")
        if next_level < 0:
            logger.debug(f" [TournamentManager] Winner {winner_id} won the tournament in room {room_id}")
            self.status[room_id] = "finished"
            #Maybe here it should trigger a reclean of the room_id so it can be reused
            return
        parent_game_id = game_id // 2
        if game_id % 2 == 0:
            logger.debug(f" [TournamentManager] parent_game_id: {parent_game_id}")
            if self.tournaments[room_id][next_level][parent_game_id]["user_left"] is not None:
                logger.debug(f" [TournamentManager] ERROR: Parent game {parent_game_id} already has a winner on the left")
            logger.debug(f" [TournamentManager] Winner {winner_id} advanced to level {next_level}, game {parent_game_id}, side left")
            self.tournaments[room_id][next_level][parent_game_id]["user_left"] = winner_id
            logger.debug(f" [TournamentManager] Winner {winner_id} advanced to level {next_level}, game {parent_game_id}, side left")
        else:
            logger.debug(f" [TournamentManager] parent_game_id: {parent_game_id}")
            if self.tournaments[room_id][next_level][parent_game_id]["user_right"] is not None:
                logger.debug(f" [TournamentManager] ERROR: Parent game {parent_game_id} already has a winner on the right")
            logger.debug(f" [TournamentManager] Winner {winner_id} advanced to level {next_level}, game {parent_game_id}, side right")
            self.tournaments[room_id][next_level][parent_game_id]["user_right"] = winner_id
            logger.debug(f" [TournamentManager] Winner {winner_id} advanced to level {next_level}, game {parent_game_id}, side right")

        logger.debug(f" [TournamentManager] Winner {winner_id} advanced to level {next_level}, game {parent_game_id})")

        # If both users for the next game are ready, start that game
        if self.tournaments[room_id][next_level][parent_game_id]["user_left"] and \
                self.tournaments[room_id][next_level][parent_game_id]["user_right"]:
            self._create_game(room_id, next_level, self.tournaments[room_id][next_level][parent_game_id]["user_left"],
                              self.tournaments[room_id][next_level][parent_game_id]["user_right"], parent_game_id)
            logger.debug(f" [TournamentManager] Created game for next level {next_level}, game {parent_game_id}")
    
    def get_tournaments(self, username):
        rooms = []
        all_rooms = self.waiting_users
        for key, value in all_rooms.items():
            players = len(value)
            joined = 'false'
            for val in value:
                if val == username:
                    joined = 'true'
                    break 
            rooms.append({'room_name': key, 'players': players, 'joined': joined })
        return { 'status': 'success', 'tournaments': rooms }

tournament_manager = TournamentManager()

#views.py

# @api_view(['POST'])
# def add_to_tournament_waiting_room(request, room_id, username):
#     logger.debug(f" [views] add_to_tournament_waiting_room: {room_id}, {username} ")
#     status = tournament_manager.add_user_to_room(room_id, username)
#     return JsonResponse({'status': status})

# @api_view(['POST'])
# def set_ready_to_play(request, room_id, username):
#     logger.debug(f" [views] set_ready_to_play: {room_id}, {username} ")
#     status = tournament_manager.user_ready_to_play(room_id, username)
#     return JsonResponse({'status': status})

# @api_view(['GET'])
# def check_tournament_waiting_room(request, room_id):
#     logger.debug(f" [views] check_tournament_waiting_room: {room_id} ")
#     response = tournament_manager.check_waiting_room(room_id)
#     return JsonResponse(response)

# @api_view(['GET'])
# def get_tournament_game(request, room_id, username):
#     logger.debug(f" [views] get_tournament_game: {room_id}, {username} ")
#     response = tournament_manager.get_game(room_id, username)
#     return JsonResponse(response)

# @api_view(['GET'])
# def get_tournament_state(request, room_id):
#     logger.debug(f" [views] get_tournament_state: {room_id} ")
#     response = tournament_manager.get_tournament_state(room_id)
#     return JsonResponse(response)
