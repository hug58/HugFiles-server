
import re

from watchdog import events
from datetime import datetime, timedelta


from utils import _files

class EventHandler(events.FileSystemEventHandler):
	"""
	Clase dedicada a los diferentes eventos del monitor de archivos,
	cada evento realiza peticiones http para subir los archivos, (GET,POST,PUT,DELETE)
	y luego envia las notificaciones al servidor para replicar los msj
	"""

	pattern = re.compile('(.+)/(.+)')

	def __init__(self):
		self.last_modified = datetime.now()
		self.message = {}

	def on_any_event(self, event):

		result = re.search(self.pattern, event.src_path)

		if datetime.now() - self.last_modified < timedelta(seconds=1):
			return
		else:
			self.last_modified = datetime.now()


		self.message = _files(event.src_path)

	
