

from flask import Flask,request,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from flask_restful import Resource, Api 

import os
import os.path
import time 

from pathlib import Path


if not os.path.isdir('data'):
	os.makedirs('data/files',exist_ok=True)

UPLOAD_FOLDER = './data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

class ListFiles(Resource):
	 
	_list_files = []

	def post(self):
		pass

	def get(self):
		for route,dirs,files in os.walk(os.path.join(UPLOAD_FOLDER,'files/') ,topdown=True):
			
			#_files = {}

			for file in files:
				
				filename = route + '/' +  file
				_file = {
					'Name': file,
					'Path': route,
					'Acces time': time.ctime(os.path.getatime(filename)),
					'Modified time': time.ctime(os.path.getmtime(filename)),
					'Change time': time.ctime(os.path.getctime(filename)),
					'Size': os.path.getsize(filename),
				}

				#_files[file] = _file
				self._list_files.append(_file)

			#self._list_files[route] = _files
			#self._list_files.append(_files)


		return jsonify(self._list_files)



class File(Resource):

	def delete(self,route):
		_route = os.path.join(UPLOAD_FOLDER,route)
		if os.path.exists(_route):
			os.remove(_route)
			return 200

		else:
			return 404



	def put(self,route):
		_route = os.path.join(UPLOAD_FOLDER,route)
		file = request.files['upload_file']
		path = Path(os.path.join(_route,file.filename) )

		if os.path.exists(path):
			file = request.files['upload_file']
			file.save(os.path.join(_route,file.filename))

			return 200
		
		else:
			return 404
	
	def post(self,route):
		_route = os.path.join(UPLOAD_FOLDER,route)

		
		'''
		Creando la carpeta sino existe
		'''
		if not os.path.isdir(_route):
			os.makedirs(_route,exist_ok=True)

		file = request.files['upload_file']
		filename = secure_filename(os.path.join(_route,file.filename))
		file.save(os.path.join(_route,filename))
		

		return jsonify(f"archivo {file.filename} subido correctamente!")


	def get(self,route):
		

		_route = os.path.join(UPLOAD_FOLDER,  route)
		path = Path(_route)


		if os.path.isfile(_route):

			try:

				return send_from_directory(
					path.parent,
					path.name,
					)

				
			except:
				
				return 404

		
		else:
			return jsonify(f'Archivo no encontrado. {_route}',404)




api.add_resource(ListFiles,
				'/',
				)


api.add_resource(File,
				'/data/<path:route>',
				)



	
if __name__ == '__main__':
	app.run(debug =  True)


