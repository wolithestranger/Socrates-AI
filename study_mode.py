import time
import threading 
import queue


class PomodoroThread(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.paused =  False
        self.stopped = False
        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
        pomodoro_cycle_count = 0
        while not self.stopped:
            pomodoro_cycle_count += 1
            self.queue.put(f"\n🍅 Starting Cycle {pomodoro_cycle_count}")
            self._countdown(300, "Break time", "🕒 Break over!")
            self.queue.put(f"Cycle {pomodoro_cycle_count} complete. Continue")

    def _countdown(self, seconds, session_type, completion_msg):
        self.queue.put(f"{session_type} started! {seconds//60} minutes left")

        for _ in range (seconds, 0, -1):
            if self.stopped: return
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
            time.sleep(1)
        self.queue.put(completion_msg)

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
    def __init__(self):
        self.queue = queue.Queue()
        self.thread = None
    
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

            except KeyboardInterrupt:
                self.thread.stop()
                break

