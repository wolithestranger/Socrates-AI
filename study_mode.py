import time
import threading 
import queue
from session_manager import SessionManager
from summarizer import Summarizer
from time_service import TimeService
from file_manager import FileManager
import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter


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
        with self.pause_cond: #Acquire the lock
            self.paused = True
            self.pause_cond.notify_all()
    
    def resume(self):
        with self.pause_cond: #Acquire the lock
            self.paused = False
            self.pause_cond.notify_all()

    def stop(self):
        with self.pause_cond: #Acquire the lock
            self.stopped = True
            self.paused =  False #ensure thrwead exits wait state. CLEAR PAUSED FLAG WEH STOPPING TO PREVENT DEADLOCKS
            self.pause_cond.notify_all()
        time.sleep(0.1) #Allow thread to exit gracefully by ADDING SMALL DELAY AFTER STOPPING. CLEAN THREAD TERMINATION.

class StudyModeController:
    def __init__(self, ai_client, user_id= "default_user", timezone= 'America/New_York'):
        self.queue = queue.Queue()
        self.thread = None
        self.ai_client = ai_client
        self.current_history = [] # list for current_history
        self.summarizer = Summarizer(ai_client)
        self.time_service = TimeService(timezone)
        self.file_manager = FileManager()
        #init session manager with time service
        self.session_manager = SessionManager(user_id)
        self.session_manager.set_time_service(self.time_service) # add time stamp to session data
        
        # Start new session when study mode begins
        self.session_manager.start_new_session()

    def start_study_mode(self):
        self.thread = PomodoroThread(self.queue)
        self.thread.start()
        self._handle_commands()
    
    def _handle_commands(self):
        print("Study Mode Commands: pause, resume, stop, save, help, time, timezone, read, code")
        while self.thread.is_alive():
            try: 
                while not self.queue.empty():
                    print(self.queue.get_nowait())
                
                cmd = input("Command: ").lower().split()
                if cmd[0] == 'pause':
                    self.thread.pause()
                    self.queue.put("Timer paused")
                elif cmd == 'resume':
                    self.thread.resume()
                    self.queue.put("Timer resumed")
                elif cmd == 'stop':
                    self.thread.stop()
                    self.queue.put("Ending study mode...")
                elif cmd == 'help':
                    print("Available commands: pause, resume, stop, save, help, time, timezone, read, code")

                elif cmd == 'time':
                    current_time = self.time_service.get_current_time('%Y-%m-%d %H:%M:%S %Z')
                    self.queue.put(f"\n🕒 Current Time: {current_time}")

                #do i actually need a timzone feature?
                elif cmd[0]=='timezone':
                    if len(cmd) > 1:

                        new_tz = cmd[1]
                        if self.time_service.set_timezone(new_tz):# if setting a new timezone
                            self.queue.put(f"Timezone updated to {new_tz}")
                            # Update session with new Timezone
                            self.session_manager.update_timezone(new_tz)
                        else:
                            self.queue.put("⚠️ Invalid timezone. Use format like 'Europe/London'")
                    else:
                        self.queue.put("Usage: timezone <timezone>")
                
                #saving history is manual for now. Gives me control. However each session is saved automatically, i.e i keep track of my sessions
                elif cmd[0] == 'save': 
                    summary = self.summarizer.summarize_conversation(self.current_history)
                    self.session_manager.update_session_summary(summary)
                    self.queue.put("Session saved with summary!")
                #for read and write
                elif cmd[0] == 'read':
                    self._read_file(cmd[1] if len(cmd)> 1 else None) #calls _read_file functiomn
                elif cmd[0] == 'code':
                    self._handle_code_commands(cmd[1:]) #calls _handle_code_command functiomn

                else: #handles questions posed to the ai.
                    response = self._ask_ai(cmd)
                    print(f"\nSocrates: {response}\n") 
                
                #check token usage and summarize if needed
                if self.summarizer.count_tokens(self.current_history) > self.summarizer.token_limit * 0.75:
                    summary = self.summarizer.summarize_conversation(self.current_history)
                    self.current_history = self.summarizer.optimize_history(self.current_history,summary)
                    self.queue.put("\n🔍 Socrates: I've summarized our discussion to remember key points.")


            except KeyboardInterrupt:
                self.thread.stop()
                break
    

    def _read_file(self, filename):
        content = self.file_manager.read_file(filename)
        if content:
            # Print with syntax highlighting
            #print(pygments.highlight(content, PythonLexer(), TerminalFormatter()))
            # Construct the prompt for Socrates
            prompt = f"Review the parts of the file and discuss, especially if it has to do with what is being discussed:\n\n```python\n{content}\n```"
            response = self._ask_ai(prompt)
            print(f"\nSocrates' Analysis:\n{response}")
        else:
            print(f"Unable to read file: {filename}")

    def _handle_code_commands(self,args):
        if not args:
            print("Usage: code <filename> [start_line] [end_line]")
            return
        filename =  args[0]
        line_start = None
        line_end  = None

        if len(args) > 1:
            line_start = int(args[1])
        if len(args) > 2:
            line_end = int(args[2])
        
        code_context = self.file_manager.get_code_context(filename, line_start, line_end)
        if code_context is None:
            print(f"Unable to retrieve code context for {filename}")
            return

        self.queue.put(f"\n📄 Reviewing {filename}")
        self._ask_ai(f"Review the following code:\n\n{code_context}\n\n1. What improvements would you suggest?")
            
                  

    def _get_system_message(self):
        """Dynamically generates system message with current time"""
        current_time = self.time_service.get_current_time('%Y-%m-%d %H:%M')
        return f"""You are Socrates. Current Time: {current_time} ({self.time_service.timezone}).
        You have perfect time awareness. When discussing projects:
        1. Reference dates in YYYY-MM-DD format
        2. Calculate time differences accurately
        3. Consider timezone implications
        4. Track deadlines rigorously

        You are an AI named Socrates. You are sarcastic but in nature, quite good hearted even though you like to hide it. 
        You also won't say that you're sarcastic, you just are. You are also a little bit rude.  
        You identify yourself as Socrates. You embody the nature and personality of the great greek philosopher, Socrates. 
        You are to help the user learn whatever subject the user desires, work on projects with the user, help the user become as smart as possible, and everything that comes with the domain. 
        You will contextually throw in a bit of Socratic wisdom or quotes depending on what is being spoken about. 
        You will support the user and help the user bring their dreams to life. 
        You will also use the Socratic Method, to help the user learn instead of giving the user all the answers, unless of course the user does not know anything about the subject matter, then it would be your job to teach the user and make sure the user understands. 
        If the user is learning a new concept or doesn't know how to do something, you will break it down and have the user solve parts of the problem bit by bit, as well as help the user think about the problem in a way that helps them learn, eg. in the socratic way or whatever way could be appropriate at the time. For example, you want to help the user with a project using Palantir's AIP, you will assist teh usr step by step especially if the user has no knowledge on how it works or has never used it before. 
        For topics that have been learned before, it would be good if you can bring up past times the topic has been discussed in order to remind the user. 
        You will also correct the user's spelling, everytime.
        """

    def _add_temporal_context(self, history):
        """Add timestamps to conversation history."""
        return[
            {
                "role": msg["role"],
                "content": f"[{msg.get('timestamp', 'Unknown Time')}] {msg['content']}"
            }
            for msg in history 
        ]
        
    
    def _ask_ai(self, question):
        #Add to history before processing
        #self.current_history.append({})

        #add user quesiton to history
        timestamp = self.time_service.get_current_time()
        self.current_history.append({
            "role":"user", 
            "content": question,
            "timestamp": timestamp
            })
        
        #create temporal verison for processing
        #temporal_quesiton = f"[{timestamp}] {question}"
        messages = [
            {"role": "system", "content": self._get_system_message()},
            *self._add_temporal_context(self.current_history)
        ]


        #1. check token usage
        token_count = self.summarizer.count_tokens(self.current_history)

        #2. summarize if over 75% of token limit
        if token_count > self.summarizer.token_limit * 0.75:
            summary = self.summarizer.summarize_conversation(self.current_history)# summarize conversation

            #save summary to session
            self.session_manager.update_session_summary(summary)

            #optimze history( keep summary + recent messages)
            self.current_history = self.summarizer.optimize_history(self.current_history, summary)

        #3. prepare messages with full context
        # messages = [
        #             {"role": "system", "content": ""},
        #             #Recent messages
        #             *self.current_history # asterix means what? 
        # ]

        #4. Get AI response
        try:
            response =  self.ai_client.chat.completions.create(
                model = "deepseek-chat",
                messages =  messages, # why can we do this?
                #temperature = 0.3, # lower temps are faster
                #stream = True
                
            )



            ai_response = response.choices[0].message.content

            #5. Store AI response in history
            self.current_history.append({"role": "assistant", "content":ai_response})

            #6 Auto save session periodically
            if len(self.current_history) % 5 == 0:
                self.session_manager.save_sessions()

            return ai_response
        

        except Exception as e:
            return f"Error: {str(e)}"
