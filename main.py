

import json
import asyncio
import websockets

import requests



USERS = set()


API = 'http://127.0.0.1:5000/api'

async def register(websocket):
	USERS.add(websocket)

async def unregister(websocket):
	USERS.remove(websocket)

async def notify_state(msg,websocket):
	
	print(msg)

	if USERS: # USERS != 0
		await asyncio.wait([ user.send(msg) for user in USERS]) #if websocket != user 


async def main(websocket,path):
	
	await register(websocket)

	'''
	petición get para obtener la lista json de todos los archivos
	'''
	
	data =requests.get(API)

	while data.status_code != 200:
		data = requests.get(API)
		await asyncio.sleep(1)

	data = data.json()

	try:
		for file in data:
			await websocket.send( json.dumps(file))

	finally:
		await unregister(websocket)



if __name__ == '__main__':

	start_server = websockets.serve(main,"localhost",7000)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()

