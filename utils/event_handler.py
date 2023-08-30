
import re
from watchdog import events
from datetime import datetime, timedelta
from utils import _files

class EventHandler(events.FileSystemEventHandler):
    """Send events to clients"""
    pattern = re.compile('(.+)/(.+)')
    def __init__(self,code=None):
        self.last_modified = datetime.now()
        self.message = {}
        self.code = code
    def on_any_event(self, event):
        """catch all events"""
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
        
        self.message = _files(event.src_path, self.code)

	
