from openai import OpenAI
from config import DEEPSEEK_API_KEY, BASE_URL, INITIAL_TASKS, INITIAL_CONSTRAINTS

class ScheduleManager:
    def __init__(self):#construtor
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url= BASE_URL) #client is just a var. What is base URL doing here 
        self.tasks = INITIAL_TASKS
        self.constraints = INITIAL_CONSTRAINTS
        self.generated_schedule = None

    def collect_additional_tasks(self):
        tasks = []
        while True:
            task = input("Enter a task (or 'done' to finish): ")
            if task.lower() =='done':
                break
            time_of_task = input("Enter time (e.g., 9 AM): ")
            duration = input("Enter duration (e.g., 1 hour): ")
            priority = input("Enter priority (high/med/low): ")
            tasks.append(f"{task}: {duration} at {time_of_task} ({priority} priority)")

        self.tasks += "\n" + "\n". join(tasks)
        
    def generate_schedule(self):
        prompt  = f"""
        Create a daily schedule based on:
        Tasks: {self.tasks}
        Constraints: {self.constraints}
        """
        

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a scheduling assistant"},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )

        self.generated_schedule = response.choices[0].message.content
        return self.generated_schedule