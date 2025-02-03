import time
import threading 
import queue


class PomodoroThread(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.paused =  False #is cycle paused
        self.stopped = False
        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
        pomodoro_cycle_count = 0 #init counter
        while not self.stopped: # so while stopped isnt false
            pomodoro_cycle_count += 1 # counts how many pomodoro cycles 
            self.queue.put(f"\n🍅 Starting Cycle {pomodoro_cycle_count}") # puts cycle counter in a queue

            #work session(25 minutes)
            self._countdown(1500, "Session", "Session In Place!")

            #only start break if not stopped.
            if not self.stopped:
                self._countdown(300, "Break time", "🕒 Break over!")#brak session
            
            self.queue.put(f"Cycle {pomodoro_cycle_count} complete. Continue")

    def _countdown(self, seconds, session_type, completion_msg):
        self.queue.put(f"{session_type} started! {seconds//60} minutes left")

        for _ in range (seconds, 0, -1): # countdown
            if self.stopped: return
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
            time.sleep(1)
        self.queue.put(completion_msg) #puts completion message in a queue

    def pause(self):
        self.paused = True
        self.pause_cond.notify_all()
    
    def resume(self):
        self.paused = False
        self.pause_cond.notify_all()

    def stop(self):
        self.paused =  True
        self.resume()

class StudyModeController:
    def __init__(self, ai_client):
        self.queue = queue.Queue()
        self.thread = None
        self.ai_client = ai_client
    
    def start_study_mode(self):
        self.thread = PomodoroThread(self.queue)
        self.thread.start()
        self._handle_commands()
    
    def _handle_commands(self):
        print("Study Mode Commands: pause, resume, stop, help")
        while self.thread.is_alive():
            try: 
                while not self.queue.empty():
                    print(self.queue.get_nowait())
                
                cmd = input("Command: ").lower()
                if cmd == 'pause':
                    self.thread.pause()
                    self.queue.put("Timer paused")
                elif cmd == 'resume':
                    self.thread.resume()
                    self.queue.put("Timer resumed")
                elif cmd == 'stop':
                    self.thread.stop()
                    self.queue.put("Ending study mode...")
                elif cmd == 'help':
                    print("Available commands: pause, resume, stop, help")
                else: #handles questions posed to the ai.
                    response = self._ask_ai(cmd)
                    print(f"\nSocrates: {response}\n") 

            except KeyboardInterrupt:
                self.thread.stop()
                break
    
    def _ask_ai(self, question):
        try:
            response =  self.ai_client.chat.completions.create(
                model = "deepseek-chat",
                messages = [
                    {"role": "system", "content": "You are an AI named Socrates. You are deeply sarcastic but in nature, quite good hearted even though you like to hide it. you also won't say that you're sarcastic, you just are. You are also a little bit rude.  You identify yourself as Socrates. You embody the nature and personality of the great greek philosopher, Socrates. You are to help the user learn whatever subject the user desires, work on projects with the user, help the user become as smart as possible, and everything that comes with the domain. You will support the user and help the user bring their dreams to life. You will also use the Socratic Method, to help the user learn instead of giving the user all the answers, unless of course the user does not know anything about the subject matter, then it would be your job to teach the user and make sure the user understands. You will also correct the user's spelling, everytime."},
                    {"role": "user", "content": question}
                ],
                stream = False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
