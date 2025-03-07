
import re
import requests
import os
import logging
from utils import get_config
from pathlib import Path

from watchdog import events
from datetime import datetime, timedelta
from urllib.parse import urljoin

from utils.api import Api

class EventHandler(events.FileSystemEventHandler):
    '''
    Class dedicated to the different events of the file monitor, each event performs http requests to upload the files, 
    (GET,POST,PUT,DELETE) and then sends the notifications to the server to replicate the messages.
    '''
    pattern = re.compile('(.+)/(.+)')
    
    def __init__(self,path, code):
        self.last_modified = datetime.now()
        self.message = {}
        self.code = code
        self.path = path
        
    def on_any_event(self, event):
        result = re.search(self.pattern, event.src_path)
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
            
        relative_path = os.path.relpath(event.src_path,self.path)
        relative_path = str(Path(relative_path).parent)
        
        
        self.message = {
			'status': event.event_type,
			'path': relative_pathh,
			'name': result.group(2),
            'hash': Api.generate_file_hash(event.src_path)
		}
        
        logging.info(f'FILE EVENT IN POLLING OBSERVER: {self.message}')
