from app import celery, socketio

@celery.task
def reply_notificacion(code, data:dict):
    '''
    Monitors the file system events of a user's 'account' (folder) and 
    then sends changes to connected clients.
    '''
    data['message'] = f"{data['type']} {data['name']} was {data['status']}"
    socketio.emit('notify', json.dumps(data), room=code)