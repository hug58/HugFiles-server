


from flask import Flask,request,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from flask_restful import Resource, Api 
from pathlib import Path

import os.path
import json


'''
por los momentos utils trae la informacion de los archivos en una lista,
la idea es guardar la informacion en una db no relacional
'''

from utils import _files
from __init__ import UPLOAD_FOLDER


#Empaquetar directorios 
import shutil



class ListFiles(Resource):
	 
	def get(self,route):

		route = os.path.join(UPLOAD_FOLDER,route)
		data = _files(route)

		
		if os.path.exists(route):


			return data,200
		else:
			return {'File no found ': route },404


class File(Resource):

	def delete(self,route):
		_route = os.path.join(UPLOAD_FOLDER,route)

		if os.path.exists(_route):

			try:
				os.remove(_route)
				return 200
				
			except PermissionError as e:
				return {'Permission Error': route },500

		else:
			return {'File no found ': route },404


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

				return 200

		else:
			return {'File no found ': route },404

	
	def post(self,route):

		_route = os.path.join(UPLOAD_FOLDER,route)

		
		'''
		Creando la carpeta sino existe
		'''

		
		if not os.path.isdir(_route):
			os.makedirs(_route,exist_ok=True)


		if not request.json:
			
			try:

				file = request.files['upload_file']
				file.save(os.path.join(_route,file.filename))
				return 201

				
			except:
				return {'File not save ': route },404


		else:
			
			return {'Dirs created ': route },201


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


		elif os.path.isdir(_route):


			return 200

			'''

				try:


					print(_route)

					print("Creando archiv..")


					basename = f'{UPLOAD_FOLDER}/temp/{path.name}' 
					filename = shutil.make_archive(basename,'zip',_route)
					print(f'creado archivo {path.name}')


					path_zip = Path(filename)


					return send_from_directory(
						path_zip.parent,
						path_zip.name,
						)



				except:
					return {'Carpeta no comprimida ':route} ,500

			'''

		else:
			return {'File no found ': route },404





if __name__ == '__main__':




	app = Flask(__name__)
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

	api = Api(app)


	api.add_resource(ListFiles,
					'/list/<path:route>',
					)
	api.add_resource(File,
					'/data/<path:route>',
					)




	#app.run(debug =  True)

	from __init__ import host_ip

	app.run(host=host_ip, port=5000)


