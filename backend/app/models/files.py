from datetime import datetime
from typing import Optional, List
from enum import Enum

from .base_model import BaseModel


class Status(Enum):
    EVENT_TYPE_MOVED = "moved"
    EVENT_TYPE_DELETED = "deleted"
    EVENT_TYPE_CREATED = "created"
    EVENT_TYPE_MODIFIED = "modified"
    EVENT_TYPE_CLOSED = "closed"
    EVENT_TYPE_OPENED = "opened"
    EVENT_TYPE_DONE = "done"
    
 

class FilesModel(BaseModel):
    
    format_str = '%Y-%m-%dT%H:%M:%S'
    
    def __init__(self, name, 
                created_at, 
                path, 
                modified_at, 
                file_hash, 
                code,
                status=Status.EVENT_TYPE_CREATED.value,
                timestamp= None
                ):
        
        self.name = name
        self.created_at = created_at
        self.path = path
        self.modified_at = modified_at
        self.file_hash = file_hash
        self.code = code
        self.status = status
        self.timestamp = timestamp


    @staticmethod
    def from_dict(data):
        return FilesModel(
            name=data.get('name'),
            created_at=data.get('created_at'),
            path=data.get('path'),
            modified_at=data.get('modified_at'),
            file_hash=data.get('file_hash'),
            code=data.get('code'),
            status= Status(data.get('status')).value,
            timestamp= data.get('timestamp')
        )


    def to_dict(self):
        return {
            'name': self.name,
            'created_at': self.created_at,
            'path': self.path,
            'modified_at': self.modified_at,
            'file_hash': self.file_hash,
            'code': self.code,
            'status': self.status,
            'timestamp': self.timestamp
        }
        
        
    @classmethod
    def find(cls, code=None, path=None, name=None):
        '''
        Search for a file by one or more of the following fields::
        - code
        - path
        - name
        '''
        query = {}  

        if code is not None:
            query["code"] = code
        if path is not None:
            query["path"] = path
        if name is not None:
            query["name"] = name

        document = cls.get_collection().find_one(query)

        if document:
            document['_id'] = str(document['_id'])
            file_model = cls.from_dict(document)
            file_model._id = document['_id'] 
            return file_model
        return None


    @classmethod
    def find_by_code_and_status(
        cls, 
        code: str, 
        exclude_status: Optional[str] = None,
        min_timestamp: Optional[datetime] = None
    ) -> List['FilesModel']:
        '''
        Searches for all files of a `code`, excludes those with the `exclude_status`,
        and filters by a minimum timestamp (if provided).
        
        :param code: The code of the file.
        :param exclude_status: The status to exclude (optional).
        :param min_timestamp: The minimum timestamp to filter by (optional).
        :return: A list of `FilesModel` instances matching the criteria.
        '''

        query = {"code": code}
        
        # Exclude files with the specified status
        if exclude_status is not None:
            query["status"] = {"$ne": exclude_status}  
        
        # Filter by minimum timestamp
        if min_timestamp is not None:
            query["timestamp"] = {"$gte": min_timestamp}

        # Execute the query
        documents = cls.get_collection().find(query)
        
        # Convert documents to FilesModel instances
        files = []
        
        print(f'DOCUMENTS: {documents}')
        
        for document in documents:
            document['_id'] = str(document['_id'])  # Convert ObjectId to string
            # file_model = cls.from_dict(document) 
            files.append(document)

        return files
    
