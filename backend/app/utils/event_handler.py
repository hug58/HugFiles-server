
import re
import pathlib
from watchdog import events
from datetime import datetime, timedelta
from .files_read import get_files, get_code_from_path

class EventHandler(events.FileSystemEventHandler):
    """Send events to clients"""
    pattern = re.compile('(.+)/(.+)')

    def __init__(self,path,code=None):
        """ EVENT HANDLER """
        self.last_modified = datetime.now()
        self.message = {}
        self.code = code
        self.path = path


    def on_any_event(self, event):
        """catch all events"""
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()

        code = get_code_from_path(self.path, event.src_path)
        self.message = get_files(event.src_path,code,status=event.event_type)


    def on_deleted(self, event:events.FileSystemEvent):
        """Catch deleted events"""
        self.message = {}
        filename = pathlib.Path(event.src_path)
        code = get_code_from_path(self.path, event.src_path)

        self.message = [{
            "name": filename.name,
            "status": event.event_type,
            "path": str(filename.parent),
            "code": code,
        }]
