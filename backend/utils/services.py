import hashlib
import os
from urllib.parse import urljoin

def workspace(email:str) -> (str,str):
    """for the moment this function saves files in local storage"""
    code =  hashlib.md5(email.encode()).hexdigest()
    path = urljoin(os.getenv('UPLOAD_FOLDER'),code)
    
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return (code,path)
    
def get_path(code:str) -> str:
    """for the moment this function saves files in local storage"""
    path = urljoin(os.getenv('UPLOAD_FOLDER'),code)
    return path
    
    
def delete(path):
    """for the moment this function deletes files in local storage"""
    return os.remove(path)