

import json
import asyncio
import websockets

import requests



USERS = set()



import socket


from __init__ import host_ip,port_api,port_ws

''' obtiene la ip de la api si se encuentra en la misma maquina,
	sino cambiarlo manualmente
'''


#host y puerto de la API
URL_API = f'http://{host_ip}:{port_api}/'




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


		try:

			data['status'] = _message['status']

			'''
			Agrega la key "oldname"
			'''

			if _message['status'] == 'renamed':
				data['oldname'] = _message['oldname']



			
		except KeyError as e:
			data = _message
			#Es una carpeta


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

	print(f'USERS: {len(USERS)}')

	'''
	petición get para obtener la lista json de todos los archivos
	'''
	

	data =requests.get(URL_API + 'list/files')
	data = data.json()

	try:


		for root in data.keys():


			_dir_root = data[root]['root'] #Enviando informacion de la carpeta
			await websocket.send( json.dumps(_dir_root) )


			for file in data[root]['files']:
				await websocket.send( json.dumps(file) )




		async for message in websocket:
			await notitfy_state(message)


	finally:
		await unregister(websocket)



if __name__ == '__main__':



	'''
	la API estará en el puerto 5000 y el ws en 7000 de la misma ip
	'''



	start_server = websockets.serve(main,host_ip,port_ws)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()

	print(__name__)