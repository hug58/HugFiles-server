import json
import os

def get_config():
    with open('config.json') as f:
        data = json.load(f)
        if not os.path.exists(data['default_folder']):
            print("Folder creation done.")
            os.makedirs(data['default_folder'])
        
        return data


def set_folder(path:str):
    data = None
    with open('config.json') as f:
        data = json.load(f)
        
    with open('config.json','w') as f:
        data['default_folder'] = path
        json.dump(data, f)
        
def set_hash_file(filename:str,path:str, hash:str):
    print(f'HASH: {hash}')
    print(f'FILENAME :: {filename}')
    
    with open('config.json','w') as f:
        files:list = data['files']
        files.append({'filename':filename, 'path':path, 'hash':hash})
        data['files'] = files
        json.dump(data, f)
    

