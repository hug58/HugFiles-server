"""
Created on Thu May 28 16:13:06 2020

@author: hug58
"""

import os
from datetime import timedelta
from datetime import datetime


from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from celery import Celery
from pymongo import MongoClient
import json


#ROUTERS
from app.routers import app_data, app_auth, app_log
#DATABASE 
from bson import ObjectId
from app.models.base_model import BaseModel

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('./utils/config.py')
app.register_blueprint(app_data, url_prefix='/data')
app.register_blueprint(app_auth, url_prefix='/token')
app.register_blueprint(app_log, url_prefix='/logs')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Sesión válida por 1 día


celery = Celery("main", broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'],)
celery.conf.update(app.config)
socketio = SocketIO(app,
    message_queue=app.config['CELERY_BROKER_URL'],
    async_mode='threading',
    cors_allowed_origins="*")


# MongoDB connection
client = MongoClient(app.config['MONGODB_URI'])
db = client['hugfiles']
BaseModel.load(db)


