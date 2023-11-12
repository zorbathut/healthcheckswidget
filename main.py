import requests
import json
import pprint

# Load API Key from config.json
try:
    with open("config.json", "r") as file:
        config = json.load(file)
        api_key = config["api_key"]
except FileNotFoundError:
    print("Error: config.json not found")
    exit()
except KeyError:
    print("Error: api_key not found in config.json")
    exit()
except json.JSONDecodeError:
    print("Error: config.json is not a valid JSON file")
    exit()

# Healthchecks.io API URL
api_url = "https://healthchecks.io/api/v1/checks/"

# Set the headers for the request
headers = {
    "X-Api-Key": api_key,
}

# Function to fetch and print the status of checks
def fetch_and_print_status():
    response = requests.get(api_url, headers=headers)
    
    # Handle the case when the request is not successful
    if response.status_code != 200:
        print(f"Failed to fetch data from Healthchecks.io: {response.status_code}")
        return
    
    data = response.json()
    checks = data['checks']

    # Filter checks that are not "up"
    failed_checks = [check for check in checks if check['status'] != "up" and check['status'] != "started"]
    
    # If there are no failed checks, print a thumbs-up emoji
    if not failed_checks:
        print("👍")
        return
    
    # If there are failed checks, print a thumbs-down emoji and the names of the failed checks
    failnames = ", ".join([check['name'] for check in failed_checks])
    print(f"👎 - {failnames}")

# Call the function to fetch and print the status
fetch_and_print_status()
