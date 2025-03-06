
from typing import Optional

import json
import os

def get_config(key:str=None, config_path:str='config.json') -> Optional[dict]:
    with open(config_path) as f:
        data = json.load(f)
        if not os.path.exists(data['default_folder']):
            print("Folder creation done.")
            os.makedirs(data['default_folder'])

        return data.get(key) if key else data


def set_folder(path:str) -> None:
    data = None
    with open('config.json') as f:
        data = json.load(f)
        
    with open('config.json','w') as f:
        data['default_folder'] = path
        json.dump(data, f)
      
  
def set_hash_file(filename: str, path: str, hash: str):
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'files': []}

    files = data['files']
    found = False
    for file in files:
        if file['filename'] == filename and file['path'] == path:
            file['hash'] = hash
            found = True
            break

    if not found:
        files.append({'filename': filename, 'path': path, 'hash': hash})

    with open('config.json', 'w') as f:
        data['files'] = files
        
        json.dump(data, f, indent=4)
    

