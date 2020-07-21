#codificar/decodificar data json
import json
#trabajar con rutas
import os.path
#comprimir archivos/copiar/mover
import shutil

from flask import Flask, render_template, request, send_from_directory, redirect, session  # jsonify

#Socketio para enviar y recibir eventos del sistema de archivos
from flask_socketio import SocketIO
from flask_socketio import emit,join_room

#Extraer rutas y nombres de archivos
import pathlib

#Ejecutar tareas en segundo plano
from celery import Celery
#############################################

from celery.task.control import revoke

#Hashes usando MD5
import hashlib


#Monitorierar eventos del sistema de archivos 
from watchdog import observers


################################################


#Listar y obtener info de los archivos y carpetas
from utils import _files,list_files,info_file
#Monitorar carpetas
from utils import event_handler




app = Flask(__name__)
app.config.from_pyfile('config.py')


celery = Celery(app.name,broker=app.config['CELERY_BROKER_URL'],backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)


socketio = SocketIO(app,
		message_queue=app.config['CELERY_BROKER_URL'],
		async_mode='threading'
		)
"""
socketio.init_app(
		app,
		message_queue=app.config['CELERY_BROKER_URL'],
		async_mode='threading'
	)
"""

tasks = {}

@celery.task
def monitor(path):
	'''
	Monitorea los eventos del sistema de archivos de una 'cuenta'(carpeta) de un usuario y luego 
	envia los cambios a los clientes conectados
	'''

	#session['id_tasks'] = self.request.id

	'''
	Error al modificar archivos desde el servidor. por revisar

	'''

	socketio = SocketIO(message_queue = app.config['CELERY_BROKER_URL']) #Conectando a la cola de mensajes de la App 


	monitorsystem = event_handler.EventHandler()
	observer = observers.Observer()

	observer.schedule(monitorsystem, path=path, recursive=True) 
	observer.start()


	print("Ruta:",path)


	try:

		while True:

			if monitorsystem.message != {}:


				_message = monitorsystem.message
				# await websocket.send(json.dumps(_message))
				#print(f'Sending... \n {_message} \n ')
				monitorsystem.message = {}
				print(_message)
				socketio.emit('files',json.dumps(_message))
				_message = {}

			else:
				pass


	except KeyboardInterrupt:
		observer.stop()

	observer.join()



@socketio.on('join')
def on_join(data):
	"""
	Accediendo a carpetas 'hasheadas'
	"""
	#mail = data['mail'] 
	main = 'prueba@mail.com'
	#mail = 'hugomontaez@gmail.com'#'soydepurbea@mail.com' #Para efectos practicos no comproborare todavia el mail
	dir_users = hashlib.md5(mail.encode()).hexdigest()
	
	path_user = os.path.join(app.config['UPLOAD_FOLDER'],'files',dir_users)

	if os.path.exists(path_user):
		emit('notify',json.dumps({
			'message':f'Correo correcto, carpeta:{dir_users}',
			'path': path_user,
			}))

		#Emitiendo info de la carpeta del usuario
		for file in _files(path_user):
			emit('files',json.dumps(file))


		#result = monitor.apply_async(args=[path_user])
		result = monitor.delay(path=path_user)
		#tasks.append({request.sid:result})
	
	else:
		emit('notify',json.dumps({'message':'Correo Incorrecto'}))


@socketio.on('disconnect')
def on_disconnect():
	'''
	Terminar tareas pendientes
	'''
	emit('notify',json.dumps({'message':f'Tasks {session["id_tasks"]} revoke '}))
	revoke(session['id_tasks'],terminate=True)
	#tasks[request.sid]

@socketio.on('notify')
def on_notify(data):
	'''
	enviar notificaciones a los clientes desktop
	'''
	emit('notify', data)


@socketio.on('files')
def handle_files(data):
	# path: Union[bytes, str] = os.path.join(app.config['UPLOAD_FOLDER'], data['data'])
	path = os.path.join(app.config['UPLOAD_FOLDER'], data['data'])
	data = _files(path)

	try:
		for file in data:
			emit('files', json.dumps(file))
	except:
		#carpeta/archivo no encontrado
		#emit('files', json.dumps({'File no found': path}))
		pass


@app.route('/data/<path:filename>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def data(filename):

	filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	path = pathlib.Path(filename)

	if request.method == 'GET':


		if os.path.isfile(filename):
			return send_from_directory(path.parent, path.name)

		elif os.path.isdir(filename):
			pass

			'''
			basename = f'{app.config["UPLOAD_FOLDER"]}/temp/{path.name}'
			_filename = shutil.make_archive(basename, 'zip', filename)

			archive = pathlib.Path(_filename)
			return send_from_directory(archive.parent, archive.name)
			'''

	elif request.method == 'POST':
		'''
		Creando la carpeta sino existe
		'''
		if not os.path.isdir(filename):
			os.makedirs(filename, exist_ok=True)

		if not request.json:

			file = request.files['upload_file']
			file.save(os.path.join(filename, file.filename))
			return redirect('/')

		else:
			return redirect('/')

	elif request.method == 'PUT':
		'''
		Comprobando si la ruta es correcta
		'''
		if os.path.exists(path):

			if os.path.isfile(path):
				'''
				Si request.json no esta vacio, cambiar nombre del archivo
				'''
				if request.json:
					data = json.loads(request.get_json())

					if data and 'new game' in data:
						new_file = str(path.parent).replace('\\', '/') + data['new game']
						os.rename(path, new_file)
						return 200
				else:
					file = request.files['upload_file']
					file.save(filename)
					return 200

			else:
				'''
				Es una carpeta
				'''

				return 200

		else:
			return {'File no found': filename}, 404

	elif request.method == 'DELETE':
		'''
		Aun falta terminar
		'''
		pass


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


if __name__ == '__main__':

	#Carpeta de prueba,
	mail = 'prueba@mail.com'
	dir_users = hashlib.md5(mail.encode()).hexdigest()
	
	#Carpeta base de los archivos del sistema y el usuario de pruebaFOUND
	os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],'files',dir_users), exist_ok=True)



	socketio.run(app, '0.0.0.0')
