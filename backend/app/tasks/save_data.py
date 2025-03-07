
import os
import json
from datetime import datetime
from bson import ObjectId


#CELERY APP
from app import celery


#MODELS
from app.models.account import Accounts 
from app.models.files import FilesModel
from app.models.files_change import FileLog


@celery.task
def save_data(file:dict):
    _id = None
    file_hash = file.get('hash')
    name = file.get('name')
    filename = os.path.join(file.get('path'), name)
    code = file.get('code')
    file_model:FilesModel = FilesModel.find(code, file.get('path'), name)
    status = file.get('status')
    modified_at = file.get('modified_at')
    file_hash = file.get('hash')

    if file_model is None:
        try: 
            _id = FilesModel(name, file.get('created_at'), file.get('path'), 
                            modified_at, file_hash,
                            code, status=status).save() 

            _id = ObjectId(_id) if isinstance(_id, str) else _id
            file_model:FilesModel = FilesModel.find(code, file.get('path'), name)
        except Exception as e:
            print(f"ERROR: {e}")
    else:
        _id = file_model._id
        
    
    
    last_log = FileLog(
        code,
        ObjectId(file_model._id),
        filename,
        status,
        file_hash if file_hash else '',
        datetime.now(),
        file.get('modified_at'))
                                
    _id_log = last_log.save()
    
    
    file_model.status = last_log.action
    file_model.id_last_log = ObjectId(_id_log)
    file_model.file_hash =  last_log.file_hash if last_log.file_hash else file_model.file_hash
    file_model.modified_at = last_log.timestamp
    FilesModel.update(_id, file_model.to_dict())
    
    
    
    
    