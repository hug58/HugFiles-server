FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Copia el archivo de requerimientos a la imagen
COPY requirements.txt .


RUN pip install --upgrade pip
RUN pip install  -r requirements.txt
RUN pip install redis
RUN pip install --no-cache-dir greenlet

COPY . .

EXPOSE 5000

