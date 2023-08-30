import json
import os.path
import shutil
import pathlib
import hashlib
import os

from flask import Flask, render_template, request, send_from_directory, redirect,jsonify
from flask_socketio import SocketIO
from flask_socketio import emit,join_room
from urllib.parse import urljoin
from celery import Celery
from celery.task.control import revoke
from watchdog import observers

from utils import _files,list_files,info_file
from utils import event_handler
from utils import services

app = Flask(__name__)
app.config.from_pyfile('config.py')
celery = Celery(app.name,broker=app.config['CELERY_BROKER_URL'],backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

socketio = SocketIO(app,
		message_queue=app.config['CELERY_BROKER_URL'],
		async_mode='threading'
		)


tasks = {}
@celery.task
def monitor(path, code):
    """
    Monitors the file system events of a user's 'account' (folder) and then sends changes to connected clients 
    sends the changes to connected clients
    """
    print("Ruta:",path)
    socket = SocketIO(message_queue = app.config['CELERY_BROKER_URL'])
    monitorsystem = event_handler.EventHandler(code)
    observer = observers.Observer()
    try:
        observer.schedule(monitorsystem, path=path, recursive=True) 
        observer.start()
        while True:
            if monitorsystem.message != {}:
                message = monitorsystem.message
                monitorsystem.message = {}
                for file in message:
                    print(file)
                    socket.emit('files',json.dumps(file), room=code)
                _message = {}
    except KeyboardInterrupt:
        observer.stop()
    except NotADirectoryError as err:
        print("error from monitor",err)
        observer.stop()
        
    observer.join()

@socketio.on('join')
def on_join(data):
    """
    Login user to monitor
    """
    code = data['code']
    path_user = urljoin(app.config['UPLOAD_FOLDER'],code)
    join_room(code)

    if os.path.exists(path_user):
        emit('notify',json.dumps({
            'message':f'Email succesfully, dir: {code}',
            'path': code,
        }))
        for file in _files(path_user, code):
            emit('files',json.dumps(file), room=code)
        monitor.delay(path=path_user, code=code)
        
    else:
	    emit('notify',json.dumps({'message':'Email is not available'}), room=code)


@socketio.on('disconnect')
def on_disconnect():
    """ Kill tasks pending"""
    try:
        emit('notify',json.dumps({'message':f'Tasks {session["id_tasks"]} revoke '}))
        revoke(session['id_tasks'],terminate=True)
    except:
        print("Failed to revoke")

@socketio.on('notify')
def on_notify(data):
    """send notifications to clients of user"""
    emit('notify', data)


@socketio.on('files')
def handle_files(data):
    """
    send notifications to clients of files
    """
    code = data['code']
    path = os.path.join(app.config['UPLOAD_FOLDER'], data['data'])
    data = _files(path,code)
    for file in data:
        emit('files', json.dumps(file), room=code)


@app.route('/data/<path:filename>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def data(filename):
    """Handle files"""
    filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    path = pathlib.Path(filename)
    if request.method == 'GET':
        if os.path.isfile(filename):
            return send_from_directory(path.parent, path.name)
        elif os.path.isdir(filename):
            return send_from_directory(path.parent, path.name)
    elif request.method == 'POST':
        if not os.path.isdir(filename): 
            os.makedirs(filename, exist_ok=True)
        
        if not request.json:
            file = request.files['upload_file']
            file.save(os.path.join(filename, file.filename))
            return jsonify({'msg':'save uploaded file'})
        else:
            return jsonify({'msg':'file not found'})
         
    elif request.method == 'PUT':
        if os.path.exists(path):
            if os.path.isfile(path):
                if request.json:
                    data = json.loads(request.get_json())
                    if data and 'name' in data:
                        new_file = str(path.parent).replace('\\', '/') + data['name']
                        os.rename(path, new_file)
                        return jsonify({'msg':'save uploaded file'})
                else:
                    request.files['upload_file'].save(filename)
                    return jsonify({'msg':'succesfully updated file'})
            else:
                return jsonify({'msg':'did not update uploaded file'})
            
        else:
            return {'File not found': filename}, 404
    elif request.method == 'DELETE':
        services.delete(filename)
        return jsonify({'msg':'deleted file'})


@app.route('/', methods=['GET', 'POST'])
def index():
    """Index the gui server web"""
    #TODO: update client web
    return render_template('index.html')

@app.route('/token', methods=['POST'])
def token():
    """Get path with token"""
    data = request.json
    if  isinstance(data,dict) != True: 
        return jsonify({'msg':'json invalid'})
    if not data['email']: 
        return jsonify({'msg':'email empty'})

    code, path = services.workspace(data['email'])
    return jsonify({'path':path,'code':code})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
