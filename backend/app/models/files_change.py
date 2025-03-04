from datetime import datetime
from bson import ObjectId
from .base_model import BaseModel

class FileLog(BaseModel):
    def __init__(self, code, id_file, filename, action, timestamp=None):
        self.code = code  # code the account
        self.filename = filename  
        self.action = action  # action done: "added", "modified", "deleted"
        self.timestamp = timestamp or datetime.now()
        self.id_file = id_file  

    @staticmethod
    def from_dict(data):
        return FileLog(
            code=data.get('code'),
            filename=data.get('filename'),
            action=data.get('action'),
            timestamp=data.get('timestamp'),
            id_file= data.get('id_file'),
        )

    def to_dict(self):
        return {
            'code': self.code,
            'filename': self.filename,
            'action': self.action,
            'timestamp': self.timestamp,
            'id_file': self.id_file
        }

    @classmethod
    def find_by_code(cls, code):
        '''Searches all logs associated with an account code.'''
        logs = cls.get_collection().find({"code": code})
        return [cls.from_dict(log) for log in logs]

    @classmethod
    def find_recent_changes(cls, code, last_sync_time):
        '''Find recent changes for an account since the last synchronization.'''
        logs = cls.get_collection().find({
            "code": code,
            "timestamp": {"$gt": last_sync_time}
        })
        return [cls.from_dict(log) for log in logs]

    @classmethod
    def find_last_changes_by_code(cls, code, last_sync_time=None):
        '''
        Finds the last change for each file associated with an account code.
        If last_sync_time is given, only changes after that date are returned.
        '''
        pipeline = [
            {"$match": {"code": code}},  
        ]

        if last_sync_time:
            pipeline[0]["$match"]["timestamp"] = {"$gt": last_sync_time}

        # Agrupa por filename y selecciona el último cambio para cada archivo
        pipeline.extend([
            {"$sort": {"timestamp": -1}}, #timestamp descending
            {
                "$group": {
                    "_id": "$filename",  # group by filename
                    "last_change": {"$first": "$$ROOT"}  # Select first element
                }
            },
            {"$replaceRoot": {"newRoot": "$last_change"}}  
        ])

        logs = cls.get_collection().aggregate(pipeline)
        return [cls.from_dict(log) for log in logs]