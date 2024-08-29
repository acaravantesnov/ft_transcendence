import websockets
import sys
import json
import asyncio
import ssl

async def main(uri):
  ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
  ssl_context.check_hostname = False
  ssl_context.verify_mode = ssl.CERT_NONE
  async with websockets.connect(uri,ssl=ssl_context, ping_interval=None, ping_timeout=None) as websocket:
    await websocket.send(json.dumps({"type": "join"}))
    while True:
      response = await websocket.recv()
      print(response)
      state = json.loads(response)
      if state['type'] == "game_state":
        if state['state']['game_over']['ended']:
          print("Game over")
          break
    # Disconnect from websocket
    # await websocket.send(json.dumps({"type": "disconnect"}))

      # speed = 0
      # move_message = json.dumps({
      #   "type": "paddle",
      #   "speed": speed
      # })
      # await websocket.send(move_message)

if __name__ == "__main__":
  uri = sys.argv[1]
  asyncio.get_event_loop().run_until_complete(main(uri))
