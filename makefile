


build-backend:
	docker build -t hugfiles-server-backend:v0 ./backend


docker: build-backend
	docker compose build 
	docker compose up -d