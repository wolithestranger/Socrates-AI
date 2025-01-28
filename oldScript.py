import os 
import requests
import json
from dotenv import load_dotenv

# Name: python-dotenv
# Version: 1.0.1
# Summary: Read key-value pairs from a .env file and set them as environment variables

load_dotenv() 
API_KEY = os.getenv("DEEPSEEK_API_KEY")

#Define task aND CONSTRAINTS

#inputData being sent to the deepseek api 

#ideally should be an empty dictionary. 

# Put in readme
# CURRENTLY THE STRUCTURE IS 2 MAIN DICTS. 1 FOR TASKS AND OTHER CONSTRAINTS
# ANOTHER FOR CONSTRAINTS
# "tasks" is key, list is values. the list is a list of dictionaries. 
# "constraints" is dict with two 3 dicts, start time, end time and recurring events
# constraints are fixed
# recurring events is a dict, with a list of dicts

schedule_data = {
    "tasks" : [
        {"name" : "Work", "duration": "4 hours", "priority" : "high"},
        {"name": "Study", "duration": "2 hours", "priority": "high"},
        {"name": "Exercise", "duration": "1 hour", "priority": "medium"},
        {"name": "Leisure", "duration": "1 hour", "priority": "low"}
    ], 
    "constraints" : { #my day starts at 9 am and ends at 9 pm
        "start_time" : "09:00", 
        "end_time" : "21:00",
        "recurring_events" : [
            {"name" : "Lunch", "time" : "12:00", "duration" : "1 hour"},
            {"name": "Dinner", "time": "18:00", "duration": "1 hour"}
        ]
    }
}

#CALL DEEPSEEK API
# Set API Endpoint and Headers

API_URL = "https://api.deepseek.com/v1/schedule"  # DeepSeek API endpoint
headers = {
    "Authorization" : f"Bearer {API_KEY}",
    "Content-Type": "application/json" #specify json data is being sent 
}

# Send the data to the API and get the response
response = requests.post(API_URL, headers=headers, data=json.dumps(schedule_data))


#check if API Cll was successful
if response.status_code == 200:
    schedule =  response.json().get("schedule", []) #extract teh schedule from response

    print("\nYour Daily Schedule: ")

    for event in schedule:
        print(f"{event['time']}: {event['task']}")  # Print each event in the schedule

else:
    #if API CALL FAILS PRINT ERROR MESAGE
    print(f"Error: {response.status_code}, {response.text}")

