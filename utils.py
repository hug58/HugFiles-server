

import os
 
def list_files(path):
	_list_files = []

	for route,dirs,files in os.walk(path,topdown=True):	
		route = route.replace('\\','/')
		for file in files:		
			filename = route + '/' +  file
			_file = {
				'Name': file,
				'Path': route,
				'Acces time': os.path.getatime(filename),
				'Modified time': os.path.getmtime(filename),
				'Change time': os.path.getctime(filename),
				'Size': os.path.getsize(filename),
			}
			_list_files.append(_file)

	return _list_files
