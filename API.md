# API Documentation

## Base URLs
- **HTTPS Base URL:** `https://ft_transcendence/users`
- **WSS Base URL:** `wss://ws/game2`

## HTTPS Endpoints

### Endpoint 1: [GET] /waitlist/checkwaitlist/\<username>/
Check if the user is still waiting on the waitlist

#### Response
If it is not in the waitlist
```json
{
  "status": "not in waitlist"
}
```
If it is waiting
```json
{
  "status": "waiting"
}
```
It it has been accepted to a game
```json
{
  "status": "success"
  "response": {
    "room_name": "room_name",
    "user_left": "username1",
    "user_right": "username2"
  } 
}
```

### Endpoint 2: [POST] /waitlist/addtowaitlist/\<username>/
It adds the user to the waitlist

#### Request Body
```json
```

#### Response
```json
{
  "status": "success"
}
```

## HTTPS Endpoints (Propostition for Tournament)

### Endpoint 1: [POST] /tournament/addtowaitingroom/\<room_id>/\<username>/
It adds the user to the tournament waiting room based on the room_id

#### Request Body
```json
```

#### Response
```json
{
  "status": "success"
}
```

if room is already playing
```json
{
  "status": "error: already in game"
}
```

### Endpoint 2: [GET] /tournament/checkwaitingroom/\<room_id>/
Check what is the waiting room of the tournament with id room_id

#### Response
If it is not in the waitlist
```json
{
  "status": "not in waitlist",
  "people waiting":
  [
    {"user_id": "username", "ready_to_play": True},
    {"user_id": "username2", "ready_to_play": False},
    ...
  ]
}
```
If it is waiting
```json
{
  "status": "waiting",
  "people waiting":
  [
    {"user_id": "username", "ready_to_play": True},
    {"user_id": "username2", "ready_to_play": False},
    ...
  ]
}
```
If every body is ready to play and a game needs to start
```json
{
  "status": "ready to play",
  "people waiting":
  [
    {"user_id": "username", "ready_to_play": True},
    {"user_id": "username2", "ready_to_play": True},
    ...
  ]
}
```

### Endpoint 3: [POST] /tournament/readytoplay/\<room_id>/\<username>/
It tells the waiting room this player is ready to play

#### Request Body
```json
```

#### Response
```json
{
  "status": "success"
}
```

if room is already playing or user is not in waiting room
```json
{
  "status": "error"
}
```

### Endpoint 4: [GET] /tournament/getgame/\<room_id>/\<username>/
Get game from the tournament. If there is still not a game because any reason it will get an error

#### Response
Game ready to dispatch
```json
{
  "status": "success",
  "response": {
    "room_name": "room_name",
    "user_left": "username1",
    "user_right": "username2"
  } 
}
```
If it should wait (for eg other user hasn't finished their match)
```json
{
  "status": "wait"
}
```
If there is a problem for eg if user is not in the torunament or it has already lost
```json
{
  "status": "error"
}
```

### Endpoint 5: [GET] /tournament/getstate/\<room_id>/
Look how the tournament is going

#### Response
If it hasn't started yet
```json
{
  "status": "waiting"
}
```
Status of the whole torunament to see how it is going while waiting
```json
{
  "status": "success",
  "n_levels": 3,
  "torunament": {
    "level_3":{
      "game_1": {
        "status": "finished",
        "winner": "username1",
        "loser": "username2"
      },
      "game_2": {
        "status": "playing",
        "user_left": "username3",
        "user_right": "username4"
      },
      "game_3": {
        "status": "skipped",
      },
      "game_4": {
        "status": "skipped",
      },
    },
    "level_2":{
      "game_1": {
        "status": "waiting",
        "user_left": "username1",
        "user_right": None,
      },
      "game_2": {
        "status": "playing",
        "user_left": "username5",
        "user_right": "username6",
      },
    },
    "level_1":{
      "game_1": {
        "status": "waiting",
        "user_left": None,
        "user_right": None,
      },
    }
  }
}
```

```


## WebSocket Endpoints

### Connection
WSS URL: `wss://game2/\<user_name>/\<room_name>/\<side>'

### Events

#### Game Update
Each frame of the game state is sent to the client at 30fps

##### Payload
TODO: Add ball velocity for AI
```json
{
  "type": "game_state"
  "state": {
    "ball_position": {
      "x": 0.5,
      "y": 0.5
    },
    "ball_speed": {
      "x": 2.0,
      "y": 2.0
    },
    "left_paddle": {
      "x": 0.5,
      "y": 0.5,
      "speed": 0.5
    },
    "right_paddle": {
      "x": 0.5,
      "y": 0.5,
      "speed": 0.5
    },
    "scores": {
      "left": 0,
      "right": 0
    },
    "game_over":{
      "ended": false,
      "winner": None
    }

  }
}
```

#### Paddle Move
When a user presses a key to move the paddle

##### Payload
```json
{
  "type": "paddle",
  "speed": 5
}
```