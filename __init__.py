



'''
Creamos la carpeta del servidor la cual serviremos los archivos
'''

import os.path
from flask_restful import Resource, Api 


UPLOAD_FOLDER = 'data'

if not os.path.isdir(UPLOAD_FOLDER):
	os.makedirs(f'{UPLOAD_FOLDER}/files',exist_ok=True)



#Configuramos el host del servidor
	
import socket

host_name = socket.gethostname()
#obtenemos la ip del servidor y luego lo pasamos a app.run
host_ip = socket.gethostbyname(host_name)


#Puerto del websocket
port_ws = 8000
#api rest
port_api = 5000