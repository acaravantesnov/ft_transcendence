import json
import asyncio
import websockets
import ssl
from agent import Agent
import time

async def game_connection(username, room_name, side, replay_buffer, wss_url):
    uri = f"{wss_url}/{username}/{room_name}/{side}/"
    print(f"Connecting to {uri}")
    agent = Agent(side, replay_buffer)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async def connect():
        try:
            async with websockets.connect(uri, ssl=ssl_context, ping_interval=None, ping_timeout=None) as websocket:
                # Send join message
                join_message = json.dumps({"type": "join"})
                await websocket.send(join_message)
                last_time = time.time()
                while True:
                    try:
                        # Receive state
                        state_message = await websocket.recv()
                        #only send a message every second
                        if time.time() - last_time > 1.0:
                          last_time = time.time()

                          state = json.loads(state_message)

                          # Decide on an action
                          if state['type'] == "game_state":
                            speed = agent.decide_action(state['state'])

                          # Send paddle move
                          move_message = json.dumps({
                              "type": "paddle",
                              "speed": speed
                          })
                          await websocket.send(move_message)

                    except websockets.exceptions.ConnectionClosed as e:
                        print(f"Connection closed: {e}")
                        break
        except Exception as e:
            print(f"Failed to connect or lost connection: {e}")

    while True:
        await connect()
        print("Reconnecting in 1 seconds...")
        await asyncio.sleep(1)

