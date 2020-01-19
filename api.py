

from flask import Flask,request,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from flask_restful import Resource, Api 
from pathlib import Path

import os.path
import json


#Locals
from utils import _files


if not os.path.isdir('data'):
	os.makedirs('data/files',exist_ok=True)

UPLOAD_FOLDER = 'data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

class ListFiles(Resource):
	 
	def get(self,route):
		route = os.path.join(UPLOAD_FOLDER,route)
		return jsonify(_files(route))

class File(Resource):

	def delete(self,route):
		_route = os.path.join(UPLOAD_FOLDER,route)

		if os.path.exists(_route):
			os.remove(_route)
			return 200

		else:
			return 400

	def put(self,route):

		_route = os.path.join(UPLOAD_FOLDER,route)
		
		path = Path(_route) 


		if os.path.exists(path):

			if os.path.isfile(path):

				if request.json:
					data = json.loads(request.get_json())   

					if data and 'new name' in data:
						new_file = str(path.parent).replace('\\','/') + '/' + data['new name']
						os.rename(_route,new_file)
						return 200

				else:
					file = request.files['upload_file']
					file.save(_route)
					return 200



			else:
				'''
				Es una carpeta
				'''

				return 202

		
		else:
			return 404
	
	def post(self,route):
		_route = os.path.join(UPLOAD_FOLDER,route)

		
		'''
		Creando la carpeta sino existe
		'''

		
		if not os.path.isdir(_route):
			os.makedirs(_route,exist_ok=True)


		try:
			
			file = request.files['upload_file']
			file.save(os.path.join(_route,file.filename))
			return 200

		except:

			return 400


	def get(self,route):
		

		_route = os.path.join(UPLOAD_FOLDER,route)
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
			return jsonify(f'file no found. {path.name}',404)




api.add_resource(ListFiles,
				'/list/<path:route>',
				)
api.add_resource(File,
				'/data/<path:route>',
				)



	
if __name__ == '__main__':
	app.run(debug =  True)


