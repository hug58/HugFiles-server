
from io import BytesIO
from PIL import Image
from datetime import datetime


try:
  from pathlib import Path
except ImportError:
  from pathlib2 import Path 


import os.path
import os 
import re
import imghdr
import  argparse
import logging
import shutil




logging.basicConfig(
	level=logging.DEBUG,
)



class CompressImage(object):

	def __init__(self,fields=['image','featured_image'],dest_backup=os.path.abspath('./BACKUP'),**kargs):

		self.fields = fields
		self.date = datetime.today().strftime('%d-%b-%Y-%H:%M:%S')
		
		self.pattern = r'.+(_BACKUP_).+\.'


		try:
			self.dest_backup = os.path.join(dest_backup,str(self.date))
			os.makedirs(_dir, exist_ok=True)
		except:
			#Python2
			pass


		'''
		RESTORE
		'''
		self.restore_path = dest_backup


		'''
		PATH PARENT
		'''
		self.parent = ''

		'''
		MODIFIED IMAGE
		'''
		self.max_size = (0,0)


		'''
		ACTIONS

		'''

		self.actions = self.validated_actions(kargs)



	def validated_actions(self,kargs):
		width = kargs.get('MAX_WIDTH')
		if width:
			self.max_size = (width,width//2)
			kargs['MODIFIED_IMAGE'] = True




		backup = kargs.get('BACKUP')
		if backup:
			if 'm' in backup:
				kargs['BACKUP_MOVE'] = True

			if 'p' in backup: 
				kargs['PREVIUS_SAVE'] = True 




		restore = kargs.get('RESTORE')
		if restore:
			self.restore_path = os.path.join(self.restore_path,restore)
			'''
			RESTORE_BACKUP not implemented yet
			'''

			kargs['RESTORE_BACKUP'] = True




		return  {
			'BACKUP': kargs.get('BACKUP',True),
			'PREVIUS_SAVE': kargs.get('PREVIUS_SAVE',False),
			'RENAME_PREFIX': kargs.get('RENAME_PREFIX',False),
			'BACKUP_MOVE': kargs.get('BACKUP_MOVE',False),
			'DELETE_BACKOUP_EXISTS': kargs.get('DELETE_BACKOUP_EXISTS',True),
			'MODIFIED_IMAGE': kargs.get('MODIFIED_IMAGE',False),
			'RESTORE_BACKUP': kargs.get('RESTORE_BACKUP',False),
		}


	@staticmethod
	def compress(path,quality=85):
		im = Image.open(path)
		# save image to object
		im.convert('RGB').save(im.filename , format='JPEG', quality=quality, optimize=True) 
		return im


	def _modified_size_image(self,size,filename,img = None,path=None):
		'''
		
		'''
		if path:
			try:
				img = Image.open(str(path))
				#path = Path(path)
			except:
				raise 'Image not found'

		if img:
			img = img.resize(size,Image.ANTIALIAS)
			img.save(filename)
			return img

		raise 'Image not found'


	def _rename_images_suffix(self,path):
		_path = Path(path)
		suffix = imghdr.what(_path)

		filename =  f'{_path.stem}.{suffix}' 

		path = os.path.join(_path.parent,filename)
		return os.rename(_path,path)


	def _rename_images_restore_backup(self,path,date):
		_path = Path(path)
		_format = "_BACKUP_{date}_".format(date =date)
		_filename = _path.name


		filename,suffix = _filename.rsplit(_format)
		return filename + suffix


	def set_restore_backup(self,dest,date):

		for root,dirs,files in os.walk(self.restore_path):
			for file in files:
				_path = os.path.join(root,file)
				
				image_dest = self._rename_images_restore_backup(_path,date)

				_dir_path = root.rsplit(Path(self.restore_path).name)[1][1:] 
				os.makedirs(_dir_path, exist_ok=True)

				dest =os.path.join(_dir_path, image_dest)
				shutil.copy(_path,dest)


	def _get_backup_one(self,path):
		if type(path) == str: path = Path(path)
		match = re.findall(self.pattern,path.name)
		'''
		shutil allows to move between disks, instead remove.os does not
		'''
		if match:

			_path = None
			if os.path.isfile(path):
				_path = path.parent

			_dir = os.path.join(self.dest_backup,_path)


			try:
				os.makedirs(_dir, exist_ok=True)
			except:
				#Python2
				pass

			
			dest = os.path.join(str(self.dest_backup),path)


			'''
			you could use shutil.move, but you risk failing and losing the original backup file
			'''
			if not os.path.exists(dest) or self.actions['DELETE_BACKOUP_EXISTS']:
				shutil.copy(path,dest)
				os.remove(path)

			else:
				logging.debug('path already exists and actions not permission')
				
		'''
		those without the __BACKUP__TIME tag will not be moved to backup
		'''			

			
	def _get_backup_all(self,route):
		pattern = r'.+(_BACKUP_).+\.'
		'''
		Search for images in folders recursively 
		'''		
		for root,dirs,files in os.walk(route):
			for file in files:
				path = Path(os.path.join(root,file))
				if imghdr.what(path):
					_get_backup_one(path)


	def _compress(self,path,quality=85,format=True):
		im = Image.open(path)
		_path = Path(path)


		if self.actions['RENAME_PREFIX']:
			self._rename_images_suffix(_path)


		if self.actions['BACKUP']:

			if not self.actions['PREVIUS_SAVE']: #and '_BACKUP_' in _path.name:
				pass

			else:
				filename = f'{_path.stem}_BACKUP_{self.date}_{_path.suffix}' 
				
				backup = os.path.join(_path.parent,filename)
			
				if not os.path.exists(backup):
					os.rename(path,backup) 

				_path = backup




			if self.actions['BACKUP_MOVE']:
				self._get_backup_one(_path)



		
		im.convert('RGB').save(im.filename , format='JPEG', quality=quality, optimize=True) 

		if self.actions['MODIFIED_IMAGE']:
			self._modified_size_image(img=im,filename=str(Path(path)),size = self.max_size)

		#imghdr.what()
		return im


	def _compress_image_to_dirs(self,route=os.path.abspath('.'),formats=['gif','jpg','png','jpeg']):
		for root,dirs,files in os.walk(str(route)):
			for file in files:
				path = os.path.join(root,file)
				if imghdr.what(path):
					
					_dir_path = root.rsplit(Path(route).name)[1][1:] 
					path = os.path.join(Path(route).name,_dir_path,file)
					self._compress(path)




def main(max_width='',path='',backup='',restore=''):
	_path = os.path.join(os.path.abspath('.'), path)
	path_backup = os.path.abspath('./BACKUP')
	

	if backup:
		if not 'd' in backup:
			input_back = input('Input dest backup (por default seria "./BACKUP"): ')
			if input_back != '':
				path_backup = input_back
				del input_back

		else:
			'''
				"d" is default path
			
			'''
			backup = backup[1:]


	else:
		'''
		means that backup will not be done, then it is False
		'''
		backup = False

	if max_width:
		max_width = int(max_width)



	compress =  CompressImage(dest_backup=os.path.abspath(path_backup), BACKUP=backup,MAX_WIDTH=max_width,RESTORE=restore)
	if restore:	
		logging.debug('Run restore')
		compress.set_restore_backup(_path,restore)

	else:
		compress._compress_image_to_dirs(_path)




if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description ='Introducir path',
		usage='%(prog)s [options] --path --backup',
		epilog='Enjoy the program! :)'
	)


	#parser = argparse.ArgumentParser()
	#parser.add_argument('--path', type=dir_path)


	# Add the arguments
	parser.add_argument('--path',
					   metavar='PATH',
					   type=str,
					   help=' example: "desktop/images" ')



	# Add the arguments
	parser.add_argument('--backup',
					   metavar='BACK',
					   type=str,
					   help=' m -- move \n p -- "generate BACKUP"')



	# Add the arguments
	parser.add_argument('--width',
					   metavar='WIDTH',
					   type=str,
					   help='Max widt: --width 600" ')



	# Add the arguments
	parser.add_argument('--restore',
					   metavar='RESTORE',
					   type=str,
					   help='--restore "15-Jul-2021-16:12:21"')



	args = parser.parse_args()


	input_path:str = args.path
	input_backup:str = args.backup
	input_width:str = args.width
	input_restore:str = args.restore


	main(path=input_path,max_width = input_width,backup=input_backup,restore=input_restore)
