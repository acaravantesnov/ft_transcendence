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