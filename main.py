

import json
import asyncio
import websockets

import requests



USERS = set()


API = 'http://127.0.0.1:5000/list/files'

async def register(websocket):
	USERS.add(websocket)

async def unregister(websocket):
	USERS.remove(websocket)

async def notitfy_state(message):
	if USERS:

		_message = json.loads(message)
		print(f"Message: {_message}")

		await asyncio.wait([ user.send(message) for user in USERS ]) #if user != websocket



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
			await websocket.send( json.dumps(file) )

		async for message in websocket:
			await notitfy_state(message)


	finally:
		await unregister(websocket)



if __name__ == '__main__':

	start_server = websockets.serve(main,"localhost",7000)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()

	print(__name__)