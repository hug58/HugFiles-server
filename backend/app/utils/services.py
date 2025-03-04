
import os
import shutil
import hashlib

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
    if os.path.isdir(path):
        return shutil.rmtree(path)

    return os.remove(path)


def generate_file_hash(filename, algorithm='sha256') -> str:
    """ Create a hash object using the specified algorithm """
    hasher = hashlib.new(algorithm)

    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(4096), b""):
            hasher.update(block)

    return hasher.hexdigest()
