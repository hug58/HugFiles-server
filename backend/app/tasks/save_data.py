import os
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
    
    print(f'STATUS FILE: {status}')
    if file_model:
        _id = ObjectId(file_model._id)
        
        file_model.size = file.get('size')
        file_model.file_hash = file.get('hash')
        file_model.modification_date = file.get('modified_at')
        file_model.status = file.get('status')
        
        try:
            FilesModel.update(_id, file_model)
        except Exception as e:
            print(f"ERROR UPDATING: {file_model}")
            
    else:
        
        try: 
            _id = FilesModel(name, file.get('created_at'), file.get('path'), 
            file.get('modified_at'), file.get('size'), file_hash, code).save() 
            _id = ObjectId(_id) if isinstance(_id, str) else _id
            
        except Exception as e:
            print(f"ERROR: {e}")
        
    
    
    data_file_log = FileLog(
        code,
        _id,
        filename,
        status,
        datetime.now())
                                
    data_file_log.save()