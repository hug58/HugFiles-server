
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
        logging.info(f'FILE EVENT IN POLLING OBSERVER: {event}')
        
        result = re.search(self.pattern, event.src_path)
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
            
        relative_path = os.path.relpath(event.src_path,self.path)
        hash_file = Api.generate_file_hash(event.src_path)
        file_db = Api.local_files.get(relative_path)
        
        if isinstance(file_db,dict) and file_db.get('hash') == hash_file:
            logging.info(f'MATCH HASH :: DATABASE LOCAL: {file_db.get("hash")} :: FILE: {hash_file}')
            return None
        
            
        self.message = {
            'status': event.event_type,
            'path': str(Path(relative_path).parent),
            'path_local': event.src_path,
            'name': result.group(2)
        }
        


    def on_deleted(self, event:events.FileSystemEvent):
        '''Catch deleted events'''
        self.message = {}
        
        relative_path = os.path.relpath(event.src_path,self.path)
        relative_path = str(relative_path)
        
        self.message = [{
            'name': path.name,
            'status': event.event_type,
            'filename': relative_path
        }]
