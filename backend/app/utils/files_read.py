"""Read files and directories"""
import os.path
import hashlib

from pathlib import Path
from . import services
from typing import Dict,List


def get_code_from_path(base_path: str, full_path: str) -> str:
    """
    Extrae el código comparando la ruta base con la ruta final.
    
    Args:
        base_path (str): Ruta base (por ejemplo, "/ruta/base").
        full_path (str): Ruta completa (por ejemplo, "/ruta/base/code123/files/document.txt").
    
    Returns:
        str: El código extraído (por ejemplo, "code123").
    
    Raises:
        ValueError: Si no se puede extraer el código.
    """
    # Normaliza las rutas para asegurar consistencia
    base_path = os.path.normpath(base_path)
    full_path = os.path.normpath(full_path)
    
    # Verifica que la ruta final comience con la ruta base
    if not full_path.startswith(base_path):
        raise ValueError("La ruta final no comienza con la ruta base.")
    
    # Elimina la ruta base de la ruta final
    relative_path = full_path[len(base_path):]
    
    # Divide la ruta relativa en partes
    parts = [part for part in relative_path.split(os.sep) if part]
    
    # El código es la primera parte de la ruta relativa
    if parts:
        return parts[0]
    else:
        raise ValueError("No se pudo extraer el código de la ruta.")


def get_files(path: str, code:str, status = None) -> List[Dict]:
    """Checks if it is a folder to get a list of info
      instead returns only a dictionary with the file info."""

    if isinstance(path,str):
        path = path[:-1] if path.endswith("/") else path

    if not os.path.isfile(path):
        return list_files(path,code)
    
    return [info_file(path,code,status)]


def list_files(path: Path, code:str) -> list:
    """List and enumerate files in a directory"""
    files = []
    try:
        for i, file in enumerate(os.listdir(path), 1):
            route =   path.replace('\\', '/') if os.name != 'posix' else path
            # filename = route + '/' + file
            filename = os.path.join(route,file)

            if os.path.isfile(filename):
                _file = info_file(filename,code)
                _file["id"] = i
                files.append(_file)
            elif os.path.isdir(filename):
                files.append(info_file(filename,code))
                # files.extend(list_files(filename,code))
        return files

    except FileNotFoundError:
        return []


def info_file(filename: str, code:str, status=None) -> dict:
    """Get the basic info of a file the replace function changes to \\ a / for windows systems"""
    _file = {}
    path = Path(filename)
    diff = os.path.relpath(path.parent, services.get_path(code))
    diff = diff if diff != "." else "/"


    hash_file:str = services.generate_file_hash(filename)

    _file = {
        'name': path.name,
		'path': str(diff),
		'created_at': round(os.path.getatime(filename)),
		'modified_at': round(os.path.getmtime(filename)),
		'size': os.path.getsize(filename),
		'status': 'done' if status is None else status,
		'type': 'file' if os.path.isfile(filename) else 'dir',
        'code': code,
        'hash': str(hash_file)
	}
    return _file


