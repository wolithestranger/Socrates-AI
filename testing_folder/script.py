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




#define init tasks and constraints
initial_tasks = """
- Work: 4 hours (high priority)
- Study: 2 hours (high priority)
- Exercise: 1 hour (medium priority)
- Leisure: 1 hour (low priority)
"""

initial_constraints = """
- Start time: 9:00 AM
- End time: 9:00 PM
- Recurring events:
  - Lunch: 12:00 PM for 1 hour
  - Dinner: 6:00 PM for 1 hour

"""

#collects input for additional tasks
def get_user_tasks():
    tasks = []
    while True:
        task =  input("Enter a task (or type done to finish): ")
        if task.lower() == 'done':
            break
        time_of_task = input("Enter the time of the task, (9 am ): ")
        duration = input ("Enter the duration of the task, (e.g 1 hour): ")
        priority = input ("Enter the priority for this task(e.g high, mid, low): ")
        #come up with way to merge this, so that the llm parses through it e.g enter a task for making breakfast
        #for molly on saturday morning, at 5am.

        tasks.append(f"{task}: {duration} at {time_of_task} ({priority} priority)")
    return "\n".join (tasks)



#Collect additional tasks from user
additional_tasks = get_user_tasks()
print("Additional tasks collected: ", additional_tasks)

all_tasks = initial_tasks + "\n" + additional_tasks


prompt = f"""
    Create a daily schedule for me based on the following tasks and constraints

    Tasks: 
    {all_tasks}

    Constraints: 
    {initial_constraints} # shouldnt there be additional constraints if need be 
"""


#CALL DEEPSEEK API

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
