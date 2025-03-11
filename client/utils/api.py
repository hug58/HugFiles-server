
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
    last_datetime = get_config('last_time')
    format_str = '%Y-%m-%dT%H:%M:%S'
    api_resource = get_config('api_resource')
    api_download = get_config('api_download')
    
    local_files:dict = {}
    
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


    @classmethod
    def load_files(cls):
        for file in get_config('files'):
            _key = file.get('path')
            cls.local_files[_key] = file
            
        logging.info(f'LOADED FILES: {cls.local_files}')



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
    def download(cls, message: Message, type_from:str='api'):
        '''Download and modified metadata files.'''
        url_file = get_config('api_download')
        path_local = cls.folder
        
        if message.get('path') != '/':
            path_local =  os.path.join(cls.folder, path_local)
            os.makedirs(path_local, exist_ok=True)
        
        
        path_cloud = os.path.join(message['path'], message['name'])
        
        logging.info(f"FILE EVENT STATUS, FROM: {type_from} : {message.get('status')} :: PATH CLOUD: {path_cloud}")

        with requests.post(url_file, json={'code': cls.code, 'filename': path_cloud}, stream=True) as r:
            r.raise_for_status()
            filename = f'{path_local}/{message.get("name")}'
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                    
            set_hash_file(pathlib.Path(filename).name, filename, message.get('file_hash'))
            cls.load_files()
        
        return None
    
    
    @staticmethod
    def send(message:dict):
        if message['status'] == 'created':
            _path = message.get('path')
            _path_local = message.get('path')
            _url = urljoin(Api.api_resource,Api.code,_path)
            
            response = requests.post(_url, 
                files = {'upload_file': open(_path_local,'rb')},
                data= {'created_at': os.path.getatime(_path_local),
                       'modified_at': os.path.getmtime(_path_local)},
                timeout=100)
            
        elif message['status'] == 'modified':
            _path = message.get('path')
            _path_local = message.get('path')
            _url = urljoin(Api.api_resource,Api.code,_path, message.get('name'))
            
            response = requests.put(_url, 
                files = {'upload_file': open(path,'rb')},
                data = {'created_at': os.path.getatime(_path_local),
                        'modified_at': os.path.getmtime(_path_local)},
                timeout=100,
                headers={'Content-Type': 'application/json'})
        
        elif message['status'] == 'deleted':
            _url = urljoin(Api.api_resource,Api.code, message.get('filename'))
            response = requests.delete(_url,timeout=100,headers={'Content-Type': 'application/json'})       

        return None


    @classmethod
    def check_last_time(cls):
        # Get the current date and time
        now = datetime.now()
        # Format it as YYYY-MM-DDTHH:MM:SS
        min_timestamp = now.strftime(cls.format_str)
        response = None
        
        if cls.last_datetime:
            logging.info(f'LAST SYNCHRONIZATION: {cls.last_datetime}')
            response = requests.get(get_config('url_files') + f'?code={cls.code}&min_timestamp={min_timestamp}', timeout=100)
            return True
        else:
            logging.info(f'FIRST SYNCHRONIZATION FILES')
            response = requests.get(get_config('url_files') + f'?code={cls.code}', timeout=100)
        
        if response is not None and response.status_code == 200:
            files = response.json().get('files')
            for file in files:
                cls.download(file)
        
        
        set_last_time(min_timestamp)
        return False