
import requests
import json
import logging
import os
import pathlib
import hashlib

from typing import TypedDict
from urllib.parse import urljoin
from datetime import datetime


from utils import get_config, set_hash_file, set_last_time




class Api:
    '''LOGIN AND ACCESS'''
    
    folder = get_config('default_folder')
    code = None
    last_datetime = get_config('last_datetime')
    
    logging.basicConfig(
        filename='event_files.log',  
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
        datefmt='%Y-%m-%d %H:%M:%S'   # Formato de la fecha
    )
    
    class Message(TypedDict):
        path: str
        name: str
        status: str
        hash: str
        modified_at: str
        created_at: str
        type: str
        
    class FileLog(TypedDict):
        code: str
        filename: str
        action: str
        timestamp: str
        id_file: str
        
    class File(TypedDict):
        name:str
        creation_date: str
        path: str
        modification_date:str
        size:str
        file_hash:str
        code:str
        status: str


    @staticmethod
    def generate_file_hash(filename, algorithm='sha256') -> str:
        '''Create a hash object using the specified algorithm'''
        
        hasher = hashlib.new(algorithm)
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(4096), b""):
                hasher.update(block)

        return hasher.hexdigest()

    
    @classmethod
    def get_token(cls, email:str) -> str:
        '''create and login user in database[dirs]'''
        
        url = get_config('url_token')
        response: requests.Response = requests.post(url, 
            json={'username': email},
            headers={'Content-Type': 'application/json'},
            timeout=10)
        
        if response.status_code == 200:
            code = response.json().get('code')
            logging.info(f'LOGIN SUCCESFULLY: {code}')
            cls.code = code
            return code
        
        logging.error(f'STATUS :: {response.status_code} :: {response.json()}')
        return ''
    
    
    @classmethod
    def download(cls, message: Message):
        '''Download and modified metadata files.'''
        url_file = get_config('api_download')
        path_local = cls.folder
        
        if message.get('path') != '/':
            path_local =  os.path.join(cls.folder, path_local)
            os.makedirs(path_local, exist_ok=True)
        
        
        path_cloud = os.path.join(message['path'], message['name'])
        logging.info(f"FILE EVENT STATUS: {message.get('status')} :: MESSAGE: {message} :: PATH CLOUD: {path_cloud}")

        with requests.post(url_file, json={'code': cls.code, 'filename': path_cloud}, stream=True) as r:
            r.raise_for_status()
            filename = f'{path_local}/{message.get("name")}'
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                    
            path_name = pathlib.Path(filename).name
            set_hash_file(path_name, filename, Api.generate_file_hash(filename))
        
        return None
    
    
    @staticmethod
    def send(message={}):
        
        if message['status'] == 'created':
            path = message['path']
            
            response = requests.post(message['url'], 
                files = {'upload_file': open(path,'rb')},
                data= {'created_at': os.path.getatime(path),
                       'modified_at': os.path.getmtime(path)},
                timeout=100)
            
        elif message['status'] == 'modified':
            path = message['path']
            response = requests.put(urljoin(message['url'],message['name']), 
                files = {'upload_file': open(path,'rb')},
                data = {'created_at': os.path.getatime(path),
                        'modified_at': os.path.getmtime(path)},
                timeout=100,
                headers={'Content-Type': 'application/json'})
        
        elif message['status'] == 'deleted':
            response = requests.delete(urljoin(message['url'],message['name']),
                timeout=100,
                headers={'Content-Type': 'application/json'})       


        return None


    @classmethod
    def check_last_time(cls):
        # Get the current date and time
        now = datetime.now()
        # Format it as YYYY-MM-DDTHH:MM:SS
        formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S")
        
        
        if cls.last_datetime:
            #last synchronization
            logging.info(f'LAST SYNCHRONIZATION: {cls.last_datetime}')
            
            response = requests.get(get_config('url_logs') + f'?last_sync_time={formatted_date}', timeout=100)
            if response.status_code == 200:
                logs = response.json()
                for log in logs:
                    logging.info("LOG: %s" % str(log))
                    
            
            set_last_time(formatted_date)
            return True
            
        
        response = requests.get(get_config('url_files') + f'?code={cls.code}', timeout=100)
        
        if response.status_code == 200:
            files = response.json().get('files')
            logging.info(f'FILE SYNCHRONIZATION START')
            
            for file in files:
                logging.info("FILE: %s" % str(file))
                cls.download(file)
        
        
        
        set_last_time(formatted_date)
        return False