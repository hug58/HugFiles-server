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
        

