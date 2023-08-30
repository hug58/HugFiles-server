import os 

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL') 
CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PORT = os.getenv('PORT')
