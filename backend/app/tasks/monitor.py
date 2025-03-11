
from app import celery
from app.utils import event_handler
from watchdog.observers import Observer

from .save_data import save_data
from .send_notify import reply_notificacion

@celery.task
def monitor_folder(path):
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
                    message = monitorsystem.message
                    for file in message:
                        file: dict
                        
                        save_data.delay(file)                        
                        reply_notificacion.delay(file["code"], {
                            'name': file.get('name'),
                            'modified_at': file.get('modified_at') if file.get('modified_at') else '',
                            'created_at': file.get('created_at') if file.get('created_at') else '',
                            'path': file.get('path'),
                            'status': file.get('status'),
                            'type': file.get('type') if file.get('type') else '',
                            'code': file.get('code'),
                            'file_hash': file.get('hash')
                        })

                    monitorsystem.message = {}
                    
        except (KeyboardInterrupt, NotADirectoryError, FileNotFoundError) as err:
            logging.error(f"MONITOR :: {err}")
            observer.stop()
    
        observer.join()
    
    except RuntimeError as err:
        logging.error(f'MONITOR IN THREAD :: {err}')