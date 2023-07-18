
import os.path
from pathlib import Path

'''
Obtener informacion de los archivos y listarlo
'''

def _files(path: str) -> dict:
	'''
	Comprueba si es una carpeta para obtener una lista de info
	en cambio devuelve solo un diccionario con la info del archivo
	'''
	if not os.path.isfile(path):
		return list_files(path)

	else:
		return info_file(path)


def list_files(path: str) -> list:
	'''
	Listar y enumerar los archivos de una carpeta
	'''
	_list_files = []

	for i, file in enumerate(os.listdir(path), 1):
		route = path.replace('\\', '/')
		filename = route + '/' + file
		_file = info_file(filename)
		_file["id"] = i
		_list_files.append(_file)
        
	return _list_files


def info_file(filename: str) -> list:
	'''
	Obtener la info basica de un archivo
	la funcion replace cambia \\ a / para sistemas windows
	'''
	_file = {}
	path = Path(filename)

	_file = {
		'name': path.name,
		'path': str(path.parent).replace('\\', '/'),
		'created_at': os.path.getatime(filename),
		'modified_at': os.path.getmtime(filename),
		'size': os.path.getsize(filename),
		'status': 'done',
		'type': 'file' if os.path.isfile(filename) else 'dir',
	}

	return [_file]