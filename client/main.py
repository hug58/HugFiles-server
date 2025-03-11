"""docstring"""

import os
import sys
import logging
import asyncio
import json
import socketio

from watchdog.observers.polling import PollingObserver
from watchdog.observers import Observer


from utils import event_handler  
from utils import actions
from utils.tui import TerminalInterface
from utils.api import Api
from utils import  set_folder, get_config

sio = socketio.AsyncClient()
data = get_config()

URL =  data.get('url')
global DEFAULT_FOLDER

@sio.on('notify')
async def on_notify(data):
    '''get all files from server'''
    
    message: Api.Message = json.loads(data)
    status = message.get('status') 
    if status:
        filename = os.path.join(DEFAULT_FOLDER, message['path'], message['name']) if message['path'] != '/' else os.path.join(DEFAULT_FOLDER, message['name'])
            
        if (message['status'] == 'created' 
            or message['status'] == 'done'
            or message['status'] == 'modified'
            or message['status'] == 'opened'
        ):
            actions.done(filename, message)

        elif message['status'] == 'delete':
            actions.deleted(filename)
            
        message = {}


@sio.event
async def connect():
    Api.check_last_time()
    print(f'CONNECTED TO SERVER: {TerminalInterface.on()}  []')


async def producer_file(message):
    '''only upload files, TODO:  deleted files.'''
    try:
        Api.send(message)
    except Exception as err:
        logging.error(f'ERROR IN OPERATIONS FILES:: {err}')


async def producer_handler(path, code):
    '''Load monitor files and send notifications.'''
    monitorsystem = event_handler.EventHandler(path, code)
    observer = PollingObserver()
    observer.schedule(monitorsystem, path=path, recursive=True)
    observer.start()
    try:
        while True:
            if monitorsystem.message != {}:
                await producer_file(monitorsystem.message)
                monitorsystem.message = {}
                
            else:
                await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


async def main():
    global DEFAULT_FOLDER
    DEFAULT_FOLDER = get_config('default_folder')
    USER = get_config('user')

    logging.info(f'DEFAULT_FOLDER: {DEFAULT_FOLDER}')
    logging.info(f'USER: {USER}')
    

    tui = TerminalInterface(DEFAULT_FOLDER, USER)
    tui.loop()

    set_folder(tui.path)

    code = tui.code
    await sio.connect(URL)
    print(f"Running code: {code}")
    await sio.emit("join",{'code':code})
    await producer_handler(DEFAULT_FOLDER,code)
    await sio.wait()


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except asyncio.exceptions.CancelledError as e:
        sys.exit(1)
