""" API HUGFILES"""

import os
from urllib.parse import urljoin
import json

from flask import jsonify
from celery.result import AsyncResult

from flask_socketio import  emit, join_room
from app.utils.files_read import get_files
from app import app, socketio, monitor, celery

@socketio.on('join')
def on_join(data_join):
    """
    Login user to monitor.
    """
    print(f"Join with client: {data_join}")
    code = data_join['code']
    path_user = urljoin(app.config['UPLOAD_FOLDER'], code)
    join_room(code)

    if os.path.exists(path_user):
        emit('notify', json.dumps({
            'message': 'Conection established',
            'path': code,
        }))

    else:
        emit('notify', json.dumps({'message': 'Email is not available'}), room=code)


@socketio.on('disconnect')
def on_disconnect():
    """ Kill tasks pending """
    pass


@socketio.on('notify')
def on_notify(data_notify):
    """ Send notifications to clients of user """
    emit('notify', data_notify)


@socketio.on('files')
def handle_files(data_token):
    """
    Send notifications to clients of files.
    """
    code = data_token['code'] if isinstance(data_token, dict) else data_token
    path_user = urljoin(app.config['UPLOAD_FOLDER'], code)
    data_handler = get_files(path_user, code)

    for file in data_handler:
        print(f"send {file.get('name')}")
        emit('files', json.dumps(file))


@app.route('/', methods=['GET', 'POST'])
def index():
    return "API HUGOS FILES"


@app.route('/tasks/monitor', methods=['GET'])
def tasks():
    """ Return a tasks monitor """

    result = monitor.delay(path = app.config['UPLOAD_FOLDER'])
    return jsonify({"message": "send task monitor", "task_id": result.id})


@app.route('/tasks/status/<task_id>')
def task_status(task_id):
    """ Return a task status """
    result = AsyncResult(task_id, app=celery)
    return jsonify({
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    })


if __name__ == '__main__':
    monitor.delay(path = app.config['UPLOAD_FOLDER'])
    socketio.run(app, host="0.0.0.0",port=app.config['PORT']
                , allow_unsafe_werkzeug=True, debug=False)
