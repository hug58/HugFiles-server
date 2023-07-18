import os 

UPLOAD_FOLDER = 'data'
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL') #redis://localhost:6379/0'
CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER_URL')#'redis://localhost:6379/1' #usar redis como memoria cached
SECRET_KEY = 'super secret!'
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PORT = os.getenv('PORT')
