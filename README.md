# HugFiles Server
servidor de archivos con sincronizacion de clientes usando Flask, Socketio, Celery y Redis

## Primero instala las dependencias en tu maquina virtual 
```bash
pip install -r requirements.txt
```

## Redis es un broker server 
Tambien necesitas instalar el broker redis
More details about redis [Redis](https://redis.io/)

### Configure config.py 

```python
UPLOAD_FOLDER = 'data' #Carpeta del servidor
CELERY_BROKER_URL = 'redis://localhost:6379/0'
SECRET_KEY = 'super secret!'
```

## Ejecute la tarea de celery 
```bash
celery worker -A App.celery --loglevel=info
```

## Ahora el servidor socketio-flask
```bash
python App.py 
``` 