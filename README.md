# HugFiles Server
file server with client synchronization using Flask, Socketio, Celery and Redis. Like dropbox

## INSTALL DEPENDENCIES
```bash
pip install -r requirements.txt
```

## Redis is a  broker server 
More details about redis [Redis](https://redis.io/)

### LOAD ENV

```env
export REDIS_HOST="127.0.0.1:6379"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/1"
export UPLOAD_FOLDER="data/files"
export SECRET_KEY="super secret key"
```

## RUN TASK CELERY 
```bash
#load your envirotments
source .env
celery worker -A main.celery --loglevel=info
```

## RUN SERVER 
```bash
python main.py 
```

## TODO
- [x] Create file
- [x] Modified file (content)
- [x] Sync with folders
- [x] Send notification to all clients for changes of files
- [x] Client terminal 
- [ ] Client web
- [ ] Delete File 
- [ ] Modified Name file
- [ ] Authentication
- [ ] Tests

