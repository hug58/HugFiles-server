import hashlib
import os
from urllib.parse import urljoin
from typing import Tuple
from .config import UPLOAD_FOLDER

def workspace(email:str) -> Tuple[str,str]:
    """for the moment this function saves files in local storage"""
    code =  hashlib.md5(email.encode()).hexdigest()
    path = urljoin(UPLOAD_FOLDER,code)
    
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return (code,path)
    
def get_path(code:str) -> str:
    """for the moment this function saves files in local storage"""
    path = urljoin(UPLOAD_FOLDER,code)
    return path
    
    
def delete(path) -> None:
    """for the moment this function deletes files in local storage"""
    return os.remove(path)