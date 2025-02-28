import json
import os 
from datetime import datetime
from time_service import TimeService

#Class for managing sssions. Each session is recorded and it stems from here. This file handeles 


class SessionManager:
    # THE CONSTRUCTOR 
    def __init__(self, user_id = "default_user"):
        self.user_id = user_id
        self.sessions = {} #dict to store sessions
        self.current_session_id = None
        self.load_sessions()
        self.time_service = None # Init time service reference
    
    def set_time_service(self, time_service):
        """Set the time service for session management."""
        self.time_service = time_service #INITIALIZES TIME SERVICE FUNCTIONALUTY 
    
    def update_timezone(self, new_timezone):
        """Update timezone for the current session."""
        if self.current_session_id and self.time_service:
            self.sessions[self.current_session_id]["timezone"] = new_timezone
            self.save_sessions

    def _get_session_file(self): #to retrive the session dict. 
        
        return f"sessions_{self.user_id}.json" #return session id
    
    def load_sessions(self): 
        if os.path.exists(self._get_session_file()): #explanatory
            with open(self._get_session_file(), 'r') as f: 
                self.sessions = json.load(f)

    def save_sessions(self):
        with open(self._get_session_file(), 'w') as f: #writing to the session file
            json.dump(self.sessions, f, indent = 2)
    
    def start_new_session(self):
        #self.current_session_id =  datetime.now() .isoformat()
        """Start a new session with timestamp and timezone."""
        if not self.time_service:
            raise ValueError("Time service not set")
        self.current_session_id= self.time_service.get_current_time('%Y%m%d-%H%M%S')
        self.sessions[self.current_session_id] = {
            "start_time" : self.time_service.get_current_time(),
            "timezone" : str(self.time_service.timezone),
            "summary" : "",
            "messages" : []
        }
        self.save_sessions()

    def update_session_summary(self, summary):
        if self.current_session_id:
            self.sessions[self.current_session_id]["summary"] = summary # add summary to summary dictionary
            self.save_sessions()
    
    def get_session_history(self):
        return self.sessions.get(self.current_session_id, {})