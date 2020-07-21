
UPLOAD_FOLDER = 'data'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1' #usar redis como memoria cached
SECRET_KEY = 'super secret!'