
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
    status = file.get('status')
    modified_at = file.get('modified_at')
    file_hash = file.get('hash')
    
    file_model:FilesModel = FilesModel.find(code, file.get('path'), name)
    

    if file_model is None:
        try: 
            _id = FilesModel(name, file.get('created_at'), file.get('path'), 
                            modified_at=modified_at, 
                            file_hash=file_hash,
                            code=code, 
                            status=status,
                            timestamp=datetime.now(),).save() 

            _id = ObjectId(_id) if isinstance(_id, str) else _id

        # except ValueError as e:
            # print(f"VALUE ERROR: {e}")

        except Exception as e:
            print(f"ERROR: {e}")
    else:
        file_model.status = status
        file_model.file_hash =  file_hash if file_hash else file_model.file_hash
        file_model.modified_at = modified_at or file_model.modified_at
        file_model.timestamp = datetime.now()
        FilesModel.update(_id, file_model.to_dict())
        
        _id = ObjectId(file_model._id) if isinstance(file_model._id, str) else file_model._id
        
    
    
    last_log = FileLog(
        code,
        _id,
        filename,
        status,
        file_hash if file_hash else '',
        datetime.now())
                                
    _id_log = last_log.save()
    
    

    
    
    
    
    