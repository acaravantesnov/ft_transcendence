import asyncio
from config import USERNAME, BUFFER_SIZE, WSS_URL
from waitlist import add_to_waitlist, check_waitlist
from replay_buffer import ReplayBuffer
from game_connection import game_connection

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

    # Create replay buffer
    replay_buffer = ReplayBuffer(BUFFER_SIZE)

    # Connect to the game
    print(f"Connecting to game: Room={ROOM_NAME}, Side={SIDE}")
    await game_connection(USERNAME, ROOM_NAME, SIDE, replay_buffer, WSS_URL)

# Run the main function
asyncio.run(main())
