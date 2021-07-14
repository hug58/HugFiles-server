
from io import BytesIO
from PIL import Image

from pathlib import Path
from datetime import datetime

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

	'''
	actions = {
		'BACKUP':True,
		'PREVIUS_SAVE':False,
		'RENAME_PREFIX':False
	}

	'''

	def __init__(self,fields=['image','featured_image'],**kargs):
		self.actions = self.validated_actions(kargs)
		self.fields = fields
		self.date = datetime.today().strftime('%Y-%m-%d')


	def validated_actions(self,kargs):
		'''
			PREVIUS_SAVE not implemented yet
		'''

		return  {
			'BACKUP': kargs.get('BACKUP',True),
			'PREVIUS_SAVE': kargs.get('PREVIUS_SAVE',False),
			'RENAME_PREFIX': kargs.get('RENAME_PREFIX',False),
			'BACKUP_MOVE': kargs.get('BACKUP_MOVE',True)
		}



	def _get_backup(self,route,dest=os.path.join(os.path.abspath('.'),'BACKUP')):
		pattern = r'.+(_BACKUP_).+\.'

		'''
		Search for images in folders recursively 
		'''		
		for root,dirs,files in os.walk(route):
			for file in files:
				path = Path(os.path.join(root,file))
				if imghdr.what(path):

					match = re.findall(pattern,path.name)
					'''
					shutil allows to move between disks, instead remove.os does not
					'''
					if match:
						if not os.path.isdir(dest):
							os.mkdir(dest)
						
						shutil.move(str(path),str(dest))







	def _compress(self,path,quality=85,format=True):
		im = Image.open(path)
		_path = Path(path)

		if not self.actions['PREVIUS_SAVE'] and '_BACKUP_' in _path.name:
			#logging.DEBUG('PREVIUS_SAVE')
			return im


		if self.actions['BACKUP']:

			filename = f'{_path.stem}_BACKUP_{self.date}_{_path.suffix}' 
			backup = os.path.join(_path.parent,filename)
			
			if not os.path.exists(backup):
				os.rename(path,backup) 


		if self.actions['RENAME_PREFIX']:
			self._rename_images_suffix(path)

		
		im.convert('RGB').save(im.filename , format='JPEG', quality=quality, optimize=True) 
		#imghdr.what()
		return im


	
	def _rename_images_suffix(self,path):
		_path = Path(path)
		suffix = imghdr.what(_path)

		filename =  f'{_path.stem}.{suffix}' 

		path = os.path.join(_path.parent,filename)
		return os.rename(_path,path)



	def _compress_image_to_dirs(self,route=os.path.abspath('.'),formats=['gif','jpg','png','jpeg']):
		for root,dirs,files in os.walk(route):
			for file in files:
				path = os.path.join(root,file)
				if imghdr.what(path):
					self._compress(path)




def main(path):
	_path = os.path.join(os.path.abspath('.'), path)
	compress =  CompressImage()

	compress._compress_image_to_dirs(_path)
	compress._get_backup(_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description ='Introducir path',
        usage='%(prog)s [options] PATH',
        epilog='Enjoy the program! :)'
    )


	#parser = argparse.ArgumentParser()
	#parser.add_argument('--path', type=dir_path)


    # Add the arguments
    parser.add_argument('PATH',
                       metavar='PATH',
                       type=str,
                       help='the path to list')

    args = parser.parse_args()

    input_path:str = args.PATH

    main(input_path)