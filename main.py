

from flask import Flask,request,jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api 

import os


UPLOAD_FOLDER = './files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

class ListFiles(Resource):

	def get(self):
		return jsonify('No hay lista')


class File(Resource):
	
	def post(self,route,filename):

		_route = os.path.join(UPLOAD_FOLDER,route)

		'''
		Creando la carpeta sino existe
		'''

		if not os.path.isdir(_route):
			os.makedirs(route,exist_ok=True)


		with open(os.path.join(_route,filename), 'wb') as f:
			f.write(request.data)

		return jsonify( f"Archivo {filename} subido" )


	def get(self,route,filename):
		
		_route = os.path.join(UPLOAD_FOLDER,route + '/' + filename)

		if os.path.isfile(_route):
			return send_from_directory(
				os.path.join(UPLOAD_FOLDER,route),
				filename,
				as_attachment=True,
				)
		else:
			return jsonify('No Encontrado')


api.add_resource(ListFiles,
				'/',
				'/files/list',
				)


api.add_resource(File,
				'/upload/<filename>',
				'/files/<path:route>/<filename>',
				)




	

"""
@app.route('/',methods = ['POST','GET'] )

def index():

	if request.method == 'POST':

		file = request.files['file']
		route =  UPLOAD_FOLDER + str(request.form['route'])

		if not os.path.isdir(route):
			os.makedirs(route,exist_ok=True)

		app.config['UPLOAD_FOLDER'] = route

		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

		return '<h1> ¡Archivo subido correctamente! </h1> <h2> :D <h2>'

	else:

		return render_template('index.html')		
"""

if __name__ == '__main__':
	app.run(debug =  True)


