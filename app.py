

from flask import Flask,request,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from flask_restful import Resource, Api 

import os
from pathlib import Path


if not os.path.isdir('data'):
	os.makedirs('data',exist_ok=True)

UPLOAD_FOLDER = './data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

class ListFiles(Resource):
	 
	_list_files = {}

	def post(self):
		pass

	def get(self):
		for route,dirs,files in os.walk(os.path.join(UPLOAD_FOLDER,'files/') ,topdown=True):
			self._list_files[route] = files

		return self._list_files




class File(Resource):
	
	def post(self,route):

		_route = os.path.join(UPLOAD_FOLDER,route)

		
		'''
		Creando la carpeta sino existe
		'''
		if not os.path.isdir(_route):
			os.makedirs(_route,exist_ok=True)

		file = request.files['upload_file']
		file.save(os.path.join(_route,file.filename))
		

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
				
				return jsonify('No enviado.')

		
		else:
			return jsonify(f'Archivo no encontrado. {_route}',404)


"""
api.add_resource(ListFiles,
				'/',
				)
"""

api.add_resource(File,
				'/data/<path:route>',
				)



	
if __name__ == '__main__':
	app.run(debug =  True)


