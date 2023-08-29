


celery:
	#load your environment before running it
	celery worker  -A app.celery --loglevel=info
