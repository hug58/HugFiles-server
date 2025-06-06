import requests
import os
import logging

import hashlib
from urllib.parse import urljoin
import pathlib

from utils import set_hash_file,get_config, delete_file_from_config
from utils.api import Api


BASE_DIR = get_config('default_folder')


def done(filename:str,message:Api.Message) -> bool:
    '''This function is responsible verify if the file exists and 
    if was created in size of the client or verify if it sent to the server'''

    if not os.path.exists(filename):
        return created(filename, message)
    
    
    elif os.path.isfile(filename):
        hash_local = Api.generate_file_hash(filename)
        if hash_local == message.get('file_hash'):
            logging.info(f'FILE WITHOUT MODIFIED: {message.get("name")}')
            return True
        #TODO: MODIFY FOR DELTA FUNCTION
        return created(filename,message)
    
    else:
        #FOR THE MOMENT... DONT DOWNLOAD DIRECTORY
        return False


def created(filename:str, message: Api.Message) -> bool:
    '''upload a file to the server'''

    Api.download(message, type_from='actions')

    if 'created_at' in message and 'modified_at' in message:
        atime = message.get('created_at')
        mtime = message.get('modified_at')
        os.utime(filename, (atime, mtime))
        logging.info(f'SAVE :: {message.get("name")}')
        return True
    return False
    

def deleted(filename: str):
    logging.info(f'START DELETE:: {filename}')
    try:
        if os.path.exists(filename):
            if os.path.isfile(filename):
                delete_file_from_config(pathlib.Path(filename).name,filename)
                os.remove(filename)
                Api.load_files()
                return True

            os.rmdir(filename)    
            return True
        return False
    except Exception as e:
        logging.error(f'EXCEPTION IN DELETE: {e}')


