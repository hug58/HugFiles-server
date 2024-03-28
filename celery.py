# celery_tasks.py

from celery import Celery
from flask import Flask

def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


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