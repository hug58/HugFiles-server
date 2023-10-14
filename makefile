


requirements:
	pip install -r requirements.txt


bootstrap: requirements
	@echo "-------------------------"
	@echo "Your environment is ready"
	@echo "Now run: make run"

celery:
	#load your environment before running it
	celery worker  -A app.celery --loglevel=info
