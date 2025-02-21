


requirements:
	pip install --upgrade pip
	pip install -r requirements.txt


bootstrap: requirements
	@echo "-------------------------"
	@echo "Your environment is ready"
	@echo "Now run: make run"

celery:
	celery -A app.celery   worker --loglevel=info


run:
	python main.py




build-backend:
	docker build -t hugfiles-server-backend:v0 ./backend


docker: build-backend
	docker compose build 
	docker compose up -d