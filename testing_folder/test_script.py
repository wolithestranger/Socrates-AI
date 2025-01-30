import os
import time
import threading
import queue  # Needed for thread-safe communication
from openai import OpenAI
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Initialize DeepSeek Client ---
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# --- Threading Components ---
class PomodoroThread(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.paused = False
        self.stopped = False
        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
        cycle_count = 0
        while not self.stopped:
            cycle_count += 1
            self.queue.put(f"\n🍅 Starting Pomodoro Cycle {cycle_count}")
            
            # Work session
            self._countdown(25*60, "Work session", "⏳ Work session complete!")
            if self.stopped:
                break
                
            # Break session
            self._countdown(5*60, "Break time", "🕒 Break time over!")
            
            self.queue.put(f"Cycle {cycle_count} complete. Start another? (yes/no)")

    def _countdown(self, seconds, session_type, completion_msg):
        self.queue.put(f"{session_type} started! {seconds//60} minutes remaining")
        for remaining in range(seconds, 0, -1):
            if self.stopped:
                return
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
            time.sleep(1)
        self.queue.put(completion_msg)

    def pause(self):
        self.paused = True
        with self.pause_cond:
            self.pause_cond.notify_all()

    def resume(self):
        self.paused = False
        with self.pause_cond:
            self.pause_cond.notify_all()

    def stop(self):
        self.stopped = True
        self.resume()  # Unpause if paused

# --- Original Scheduling Code ---
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

def get_user_tasks():
    tasks = []
    while True:
        task = input("Enter a task (or type 'done' to finish): ")
        if task.lower() == 'done':
            break
        time_of_task = input("Enter the time of the task (e.g., 9 AM): ")
        duration = input("Enter the duration (e.g., 1 hour): ")
        priority = input("Enter priority (high/med/low): ")
        tasks.append(f"{task}: {duration} at {time_of_task} ({priority} priority)")
    return "\n".join(tasks)

# --- Integrated Study Mode ---
def study_mode():
    q = queue.Queue()
    print("\n🚀 Pomodoro Study Mode Controls 🚀")
    print("----------------------------------")
    print("Available commands during session:")
    print("- pause: Pause current session")
    print("- resume: Resume paused session")
    print("- stop: End study mode")
    print("- help: Show these commands\n")
    
    pomodoro_thread = PomodoroThread(q)
    pomodoro_thread.start()
    
    while pomodoro_thread.is_alive():
        try:
            # Process queue messages
            while not q.empty():
                print(q.get_nowait())
            
            # Check for user input
            user_input = input("Enter command (or 'help' for options): ").lower()
            
            if user_input == 'pause':
                pomodoro_thread.pause()
                q.put("Timer paused")
            elif user_input == 'resume':
                pomodoro_thread.resume()
                q.put("Timer resumed")
            elif user_input == 'stop':
                pomodoro_thread.stop()
                q.put("Ending study mode...")
            elif user_input == 'help':
                print("\nAvailable commands:")
                print("pause - Pause current session")
                print("resume - Resume paused session")
                print("stop - End study mode")
                print("help - Show this help\n")
            
        except KeyboardInterrupt:
            pomodoro_thread.stop()
            break

# --- Main Execution Flow ---
if __name__ == "__main__":
    # Get user tasks
    additional_tasks = get_user_tasks()
    all_tasks = initial_tasks + "\n" + additional_tasks

    # Generate schedule
    prompt = f"""
    Create a daily schedule for me based on the following tasks and constraints

    Tasks: 
    {all_tasks}

    Constraints: 
    {initial_constraints}
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates daily schedules."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )

    # Show schedule
    print("\nGenerated Schedule:")
    print(response.choices[0].message.content)

    # Start study mode if requested
    study_mode_choice = input("\nWould you like to start study mode now? (yes/no): ").lower()
    if study_mode_choice == 'yes':
        study_mode()