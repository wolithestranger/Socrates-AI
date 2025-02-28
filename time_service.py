from datetime import datetime
import pytz#python timezone 

class TimeService:
    def __init__(self, timezone = 'UTC'):
        self.timezone = pytz.timezone(timezone)
    
    def get_current_time(self,  fmt='%Y-%m-%d %H:%M:%S'):
        return datetime.now(self.timezone).strftime(fmt)
    
    def get_relative_time(self, base_time = None):# taking in base time as param
        now =  datetime.now(self.timezone)
        if base_time:
            return now - base_time
        return now
    
    def set_timezone(self, new_timezone):
        try:
            self.timezone = pytz.timezone(new_timezone)
            return True
        except pytz.UnknownTimeZoneError:
            return False
        