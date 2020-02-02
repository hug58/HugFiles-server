

import json
import asyncio
import websockets

import requests



USERS = set()


URL_API = 'http://127.0.0.1:5000/'
API = 'http://127.0.0.1:5000/list/files'

async def register(websocket):
	USERS.add(websocket)

async def unregister(websocket):
	USERS.remove(websocket)

async def _data(_message):

	filename = _message['path'] + '/' +  _message['name']
	url = URL_API + filename.replace('data/files/','list/files/')

	'''
	obteniendo la data del file de la API
	'''


	r = requests.get(url,timeout=5)

	'''
	actualizando el status
	'''

	data = {}

	if r.status_code == 200:

		data = r.json()	

		
		data['status'] = _message['status']

		'''
		Agrega la key "oldname"
		'''

		if _message['status'] == 'renamed':
			data['oldname'] = _message['oldname']

	else:
		data = _message


	return data


async def notitfy_state(message):

	if USERS:

		_message = json.loads(message)
		data = await _data(_message)
		message = json.dumps(data)


		await asyncio.wait([ user.send(message) for user in USERS ]) 



async def main(websocket,path):
	
	await register(websocket)

	'''
	petición get para obtener la lista json de todos los archivos
	'''
	
	data =requests.get(API)
	data = data.json()

	try:


		for root in data.keys():
			for file in data[root]:
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