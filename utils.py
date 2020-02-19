


import os
from pathlib import Path

 
def _files(path):

	if not os.path.isfile(path):
		return list_files(path)

	else:
		return info_file(path)


def list_files(path):
	
	_list_files = []
	_dirs = {}
	root = {}


	for route,dirs,files in os.walk(path,topdown=True):	
		route = route.replace('\\','/')

		for file in files:		
			
			filename = route + '/' +  file
			_file = info_file(filename)
			_list_files.append(_file) 




		_dirs[route] = {}



		#Lista de archivos

		_dirs[route]['files'] = _list_files

		root = info_file(route)



		#Indexando data de la carpeta root


		_dirs[route]['root'] = root

		_list_files = []


	return _dirs



def info_file(filename):

	_file = {}
	path = Path(filename)

	_file = {
		'name': path.name,
		'path': str(path.parent).replace('\\','/'),
		'acces time': os.path.getatime(filename),
		'modified time': os.path.getmtime(filename),
		'size': os.path.getsize(filename),
		'status': 'done',
	}

	return _file

