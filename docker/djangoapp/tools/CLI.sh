#!/bin/bash

# Configuration variables
BASE_URL="https://localhost:8080"
USERNAME="CLI"
WSS_URL="wss://localhost:8080/ws/game2"
ROOM_NAME=""
SIDE=""

# Function to add to the waitlist and check status
add_and_check_waitlist() {
    # Add to the waitlist
    echo "Adding to waitlist..."
    curl -s -X POST "$BASE_URL/users/waitlist/addtowaitlist/$USERNAME/" -H "Content-Type: application/json" -k

    # Poll the waitlist status until successful
    echo "Checking waitlist status..."
    while true; do
        response=$(curl -s "$BASE_URL/users/waitlist/checkwaitlist/$USERNAME/" -k)
        status=$(echo "$response" | jq -r '.status')

        if [ "$status" == "success" ]; then
            ROOM_NAME=$(echo "$response" | jq -r '.response.room_name')
            USER_LEFT=$(echo "$response" | jq -r '.response.user_left')

            if [[ "$USER_LEFT" == "$USERNAME" ]]; then
                SIDE="left"
            else
                SIDE="right"
            fi
            break
        fi
        echo "Waiting for room assignment..."

        sleep 1
    done
}

# Function to connect to the WebSocket, send messages, and print responses
connect_to_game() {
    uri="$WSS_URL/$USERNAME/$ROOM_NAME/$SIDE/"
    echo "Connecting to $uri"

    # Send join message and paddle speed
    # echo '{"type": "join"}' | ws text "$uri"
    # echo '{"type": "paddle", "speed": 0}' | ws text "$uri"
    # ws text "$uri" '{"type": "join"}'
    # ws text "$uri" '{"type": "paddle", "speed": 3}'

    # Listen for messages and print them
    # ws listen "$uri"
    # wscat -c  -n "$uri"
  python3 wscat.py "$uri"
}

# Main script execution
add_and_check_waitlist
echo "Connecting to game: Room=$ROOM_NAME, Side=$SIDE"
connect_to_game
