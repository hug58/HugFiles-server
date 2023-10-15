


requirements:
	pip install --upgrade pip
	pip install -r requirements.txt


bootstrap: requirements
	@echo "-------------------------"
	@echo "Your environment is ready"
	@echo "Now run: make run"

celery:
	celery worker  -A main.celery --loglevel=info


run:
	python main.py