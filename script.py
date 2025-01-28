


import os 
from openai import OpenAI
from dotenv import load_dotenv

# Name: python-dotenv
# Version: 1.0.1
# Summary: Read key-value pairs from a .env file and set them as environment variables

load_dotenv() 

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = "https://api.deepseek.com"   
)



#Define task aND CONSTRAINTS as prompt
#inputData being sent to the deepseek api 

prompt = """

Create a daily schedule for me based on the following tasks and constraints:

Tasks:
- Work: 4 hours (high priority)
- Study: 2 hours (high priority)
- Exercise: 1 hour (medium priority)
- Leisure: 1 hour (low priority)

Constraints:
- Start time: 9:00 AM
- End time: 9:00 PM
- Recurring events:
  - Lunch: 12:00 PM for 1 hour
  - Dinner: 6:00 PM for 1 hour

"""

#ideally should be an empty dictionary. 

# Put in readme
# CURRENTLY THE STRUCTURE IS 2 MAIN DICTS. 1 FOR TASKS AND OTHER CONSTRAINTS
# ANOTHER FOR CONSTRAINTS
# "tasks" is key, list is values. the list is a list of dictionaries. 
# "constraints" is dict with two 3 dicts, start time, end time and recurring events
# constraints are fixed
# recurring events is a dict, with a list of dicts



#CALL DEEPSEEK API
# Set API Endpoint and Headers


response = client.chat.completions.create(
    model = "deepseek-chat", 
    messages = [
        {"role": "system", "content" : "You are a helpful assistant that creates daily schedules."},
        {"role": "user", "content": prompt}
    ],
    stream= False
)

#print generated schedule
print(response.choices[0].message.content)


