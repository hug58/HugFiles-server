import json
import pathlib
import os
import time
from urllib.parse import urljoin

from flask import Flask, render_template, request, send_from_directory, redirect,jsonify
from flask_socketio import SocketIO
from flask_socketio import emit,join_room
from celery import Celery,Task
from watchdog import observers
from watchdog.observers.polling import PollingObserver
from utils import _files,event_handler, services

class FlaskTask(Task):
    def __call__(self, *args: object, **kwargs: object) -> object:
        with app.app_context():
            return self.run(*args, **kwargs)

app = Flask(__name__)

app.config.from_pyfile('config.py')

print(f"app config: {app.config}")
print(f"broken: {app.config['CELERY_BROKER_URL']}")
print(f"result: {app.config['CELERY_RESULT_BACKEND']}")

celery = Celery(app.import_name,broker=app.config['CELERY_BROKER_URL'],
                backend=app.config['CELERY_RESULT_BACKEND'], task_cls=FlaskTask)
celery.conf.update(app.config)

socketio = SocketIO(app,
		message_queue=app.config['CELERY_BROKER_URL'],
		async_mode='threading'
		)


tasks = {}
@celery.task
def monitor(path, code):
    """
    Monitors the file system events of a user's 'account' (folder) and 
    then sends changes to connected clients sends the changes to connected clients
    """
    print("path:",path)
    socket = SocketIO(message_queue = app.config['CELERY_BROKER_URL'])
    monitorsystem = event_handler.EventHandler(path,code)
    observer = PollingObserver()
    try:
        observer.schedule(monitorsystem, path=path, recursive=True)
        observer.start()
        while True:
            if monitorsystem.message:
                message = monitorsystem.message
                monitorsystem.message = {}
                for file in message:
                    socket.emit('files',json.dumps(file), room=code)
                _message = {}
            time.sleep(2)
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
    #TODO: remove 
    pass


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
    path =  urljoin(app.config['UPLOAD_FOLDER'],code)
    
    data = _files(path,code)
    for file in data:
        emit('files', json.dumps(file), room=code)


@app.route('/data/<path:filename>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def data(filename):
    """Handle files"""
    filename = urljoin(app.config['UPLOAD_FOLDER'], filename)

    path = pathlib.Path(filename)
    if request.method == 'GET':
        if os.path.isfile(filename):
            print("is a file")
            send_from_directory(path.parent, path.name)   
            return send_from_directory(path.parent, path.name)
        elif os.path.isdir(filename):
            # return jsonify({'msg':'is a directory'})
            print(f"name is {path.name}")
            return  json.dumps(_files(path.parent,"f1f58e8c06b2a61ce13e0c0aa9473a72"))
        
        return jsonify({"msg":"account does not exist"})
    elif request.method == 'POST':
        if not os.path.isdir(filename): 
            os.makedirs(filename, exist_ok=True)

        if 'upload_file' not in request.files:
            return 'No file part in the request'

        file = request.files['upload_file']
        file.save(os.path.join(filename, file.filename))
        return jsonify({'msg':'save uploaded file'})
         
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
                    modified_at = round(os.path.getmtime(filename))
                    os.utime(filename, (modified_at,modified_at))
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
    data_token = request.json
    if  isinstance(data_token,dict) is not True:
        return jsonify({'msg':'json invalid'})
    if not data_token['email']:
        return jsonify({'msg':'email empty'})

    code, path = services.workspace(data_token['email'])
    return jsonify({'path':path,'code':code})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0",allow_unsafe_werkzeug=True,debug=False)
