import requests
import os
import logging

import hashlib
from urllib.parse import urljoin
import pathlib

from utils import set_hash_file,get_config
from utils.api import Api


BASE_DIR = get_config('default_folder')


def done(filename:str,message:Api.Message) -> bool:
    '''This function is responsible verify if the file exists and 
    if was created in size of the client or verify if it sent to the server'''
    
    if not os.path.exists(filename):
        return created(filename, message)
    
    elif os.path.isfile(filename):
        hash_local = Api.generate_file_hash(filename)
        if hash_local == message.get('hash'):
            logging.info(f'File without modified {message.get("name")}')
            return True
        #TODO: MODIFY FOR DELTA FUNCTION
        return created(filename,message)
    
    else:
        #FOR THE MOMENT... DONT DOWNLOAD DIRECTORY
        return False


def created(filename:str, message: Api.Message) -> bool:
    '''upload a file to the server'''

    Api.download(message)

    if 'created_at' in message and 'modified_at' in message:
        atime = message.get('created_at')
        mtime = message.get('modified_at')
        os.utime(filename, (atime, mtime))
        Api.logging.info(f'SAVE :: {message.get("name")}')
        return True
    return False
    

def deleted(filename: str):
    if os.path.exists(filename):
        if os.path.isfile(filename):
            os.remove(filename)
            return True

        os.rmdir(filename)    
        return True
    return False


