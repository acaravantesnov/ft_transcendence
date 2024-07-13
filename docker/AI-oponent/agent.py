import requests
import json
import random
import asyncio
import websockets
import ssl

# Configuration
#BASE_URL = "https://ft_transcendence"
BASE_URL = "https://localhost:8080"
WSS_URL = "wss://localhost:8080/ws/game2"
USERNAME = "AI"
# USERNAME = "digarcia"
ROOM_NAME = None
SIDE = None

# Function to add user to the waitlist
def add_to_waitlist(username):
    url = f"{BASE_URL}/users/waitlist/addtowaitlist/{username}/"
    response = requests.post(url, json={}, verify=False)
    # If error, return None
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

# Function to check waitlist status
def check_waitlist(username):
    url = f"{BASE_URL}/users/waitlist/checkwaitlist/{username}/"
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

# Agent class
class Agent:
    def __init__(self, side):
        self.side = side
        self.speed = 0

    def decide_action(self):
        # Randomly choose an action: -5 (up), 5 (down), or 0 (stop)
        self.speed = random.choice([-5, 0, 5])

    def receive_state(self, state):
        # Print the received game state
        print(json.dumps(state, indent=2))

# Function to handle WebSocket connection
async def game_connection(username, room_name, side):
    uri = f"{WSS_URL}/{username}/{room_name}/{side}/"
    print(f"Connecting to {uri}")
    agent = Agent(side)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE


    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        # Send join message
        join_message = json.dumps({"type": "join"})
        await websocket.send(join_message)
        while True:
            # Receive state
            state_message = await websocket.recv()
            state = json.loads(state_message)
            agent.receive_state(state)

            # Decide on an action
            agent.decide_action()

            # Send paddle move
            move_message = json.dumps({
                "type": "paddle",
                "speed": agent.speed
            })
            await websocket.send(move_message)

            # Wait for 1 second
            await asyncio.sleep(1)

# Main function
async def main():
    # Add to waitlist
    print("Adding to waitlist...")
    add_response = add_to_waitlist(USERNAME)
    print(add_response)

    # Check waitlist status
    print("Checking waitlist status...")
    while True:
        status_response = check_waitlist(USERNAME)
        print(status_response)

        if status_response["status"] == "success":
            global ROOM_NAME, SIDE
            ROOM_NAME = status_response["response"]["room_name"]
            SIDE = "left" if status_response["response"]["user_left"] == USERNAME else "right"
            break

        await asyncio.sleep(1)

    # Connect to the game
    print(f"Connecting to game: Room={ROOM_NAME}, Side={SIDE}")
    await game_connection(USERNAME, ROOM_NAME, SIDE)

# Run the main function
asyncio.run(main())
