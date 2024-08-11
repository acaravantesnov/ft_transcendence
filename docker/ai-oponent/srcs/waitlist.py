import requests
from config import BASE_URL

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
  