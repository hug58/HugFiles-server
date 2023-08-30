
import os.path
from pathlib import Path
from . import services 

def _files(path: str, code:str) -> list:
    """Checks if it is a folder to get a list of info instead returns only a dictionary with the file info."""
    if not os.path.isfile(path):
        return list_files(path,code)
    
    return [info_file(path,code)]


def list_files(path: str, code:str) -> list:
    """List and enumerate files in a directory"""
    files = []
    for i, file in enumerate(os.listdir(path), 1):
        route = path.replace('\\', '/')
        filename = route + '/' + file
        if os.path.isfile(filename):
            _file = info_file(filename,code)
            _file["id"] = i
            files.append(_file)
        elif os.path.isdir(filename):
            files.extend(list_files(filename,code))

 
    return files


def info_file(filename: str, code:str) -> list:
    """Get the basic info of a file the replace function changes to \\ a / for windows systems"""
    _file = {}
    path = Path(filename)
    diff = os.path.relpath(path.parent,services.get_path(code))
    diff = diff if diff != "." else ""
    
    _file = {
        'name': path.name,
		'path': str(diff),
		'created_at': os.path.getatime(filename),
		'modified_at': os.path.getmtime(filename),
		'size': os.path.getsize(filename),
		'status': 'done',
		'type': 'file' if os.path.isfile(filename) else 'dir',
        'code': code,
	}
    return _file