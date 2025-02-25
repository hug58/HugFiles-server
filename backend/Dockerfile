FROM python:3.9-slim-buster
# RUN apt-get update && apt-get install -y build-essential

# Instala curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia el archivo de requerimientos a la imagen
COPY requirements.txt .

COPY start_celery.sh /start_celery.sh
RUN chmod +x /start_celery.sh

RUN pip install --upgrade pip
RUN pip install  -r requirements.txt
RUN pip install redis

COPY . .



EXPOSE 8000

