


from flask import Flask, render_template


'''
Traemos las clases de las apis
'''

from api import ListFiles,File

'''
La carpeta que contiene los archivos y el host publico
'''
from __init__ import *




app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html',host_ip= host_ip, port_ws = port_ws)






app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


api = Api(app)


api.add_resource(ListFiles,'/list/<path:route>',)
api.add_resource(File,'/data/<path:route>',)



if __name__ == '__main__':







	#app.run(debug =  True)

	from __init__ import host_ip

	app.run(host=host_ip, port=5000)
