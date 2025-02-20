"""docstring"""

import os
import asyncio
import json
import socketio

from watchdog.observers.polling import PollingObserver

from utils import event_handler  
from utils import actions
from utils.tui import TerminalInterface
from utils.api import Api
from utils import  set_folder, get_config

sio = socketio.AsyncClient()
data = get_config()

URL =  data['url']
API_DOWNLOAD = data['api_download']

global DEFAULT_FOLDER

@sio.on('notify')
async def on_notify(data):
    """ get all files from server """
    global result
    result = ''
    try:
        message: dict = json.loads(data)

        if message.get("status"):
            message['path_user_local'] = os.path.join(DEFAULT_FOLDER, message['path'])
            if message['status'] == 'created' or message['status'] == 'done':
                result = actions.done(API_DOWNLOAD,message)
            elif message['status'] == 'modified':
                if actions.modified(data): 
                    result = actions.created(API_DOWNLOAD,message)
            elif message['status'] == 'delete':
                    result = actions.deleted(message)
            
            message = None

        print(f"MESSAGE: {message['message']}")
        
    except TypeError as err:
        pass


async def producer_file(message):
    """ only upload files, TODO:  deleted files"""
    print(f"url dir :: {message['url']}")

    if message['status'] == 'created':
        Api.send(message=message)
    elif message['status'] == 'modified':
        try:
            Api.send("PUT",message)
        except os.IsADirectory as err:
            print(err)
    elif message['status'] == 'deleted':
        Api.send("DELETE",message)


async def producer_handler(path, code):
    """Load monitor files and send notifications"""
    monitorsystem = event_handler.EventHandler(path, code)
    observer = PollingObserver()
    observer.schedule(monitorsystem, path=path, recursive=True)
    observer.start()
    print('Loading Monitorsystem')
    
    while True:
        if monitorsystem.message != {}:
            _message = monitorsystem.message
            monitorsystem.message = {}
            await producer_file(_message)
        else:
            await asyncio.sleep(1)


async def main():
    global DEFAULT_FOLDER
    DEFAULT_FOLDER = get_config()['default_folder']
    USER = get_config()['user']

    tui = TerminalInterface(DEFAULT_FOLDER, USER)
    tui.loop()

    set_folder(tui.path)

    code = tui.code
    await sio.connect(URL)
    print(f"Running code: {code}")
    await sio.emit("join",{'code':code})
    await producer_handler(DEFAULT_FOLDER,code)
    await sio.wait()

    print("Exiting...")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
