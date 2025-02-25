"""
Created on Thu May 28 16:13:06 2020

@author: hug58
"""

import json

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from celery import Celery
from watchdog.observers import Observer

from app.utils import event_handler
from app.routers import app_data, app_auth

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('./utils/config.py')
app.register_blueprint(app_data, url_prefix='/data')
app.register_blueprint(app_auth, url_prefix='/token')


celery = Celery("main", broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'],)
celery.conf.update(app.config)
socketio = SocketIO(app,
    message_queue=app.config['CELERY_BROKER_URL'],
    async_mode='threading',
    cors_allowed_origins="*")


# MongoDB connection
# from pymongo import MongoClient
# client = MongoClient('mongodb://localhost:27017/')
# db = client['mydatabase']  # Replace 'mydatabase' with your database name
# collection = db['mycollection']  # Replace 'mycollection' with your collection name


@celery.task
def monitor(path):
    '''
    Monitors the file system events of a user's 'account' (folder) and 
    then sends changes to connected clients.
    '''
    monitorsystem = event_handler.EventHandler(path)
    observer = Observer()

    try:
        try:    
            print(f'Monitoring START: {path}')
            observer.schedule(monitorsystem, path=path, recursive=True)
            observer.start()
            while True:
                if monitorsystem.message:
                    print(f'monitoring: {monitorsystem.message}')
                    message = monitorsystem.message
                    for file in message:
                        file: dict
                        reply_notificacion.delay(file["code"], {
                            'name': file['name'],
                            'modified_at': file.get('modified_at') if file.get('modified_at') else '',
                            'created_at': file.get('created_at') if file.get('created_at') else '',
                            'path': file['path'],
                            'status': file['status'],
                            'type': file.get('type') if file.get('type') else '',
                            'code': file['code'],
                            'hash': file.get('hash')
                        })

                    monitorsystem.message = {}
                    
        except (KeyboardInterrupt, NotADirectoryError, FileNotFoundError) as err:
            print(f"Error from monitor :::: {err}")
            observer.stop()
    
        observer.join()
    
    except RuntimeError as err:
        print(f'Error from monitor in thread :::: {err}')


@celery.task
def reply_notificacion(code, data:dict):
    """
    Monitors the file system events of a user's 'account' (folder) and 
    then sends changes to connected clients.
    """
    data['message'] = f"{data['type']} {data['name']} was {data['status']}"
    socketio.emit('notify', json.dumps(data), room=code)
