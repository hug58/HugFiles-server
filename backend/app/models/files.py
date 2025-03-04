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
 

class FilesModel(BaseModel):
    def __init__(self, name, 
                creation_date, 
                path, 
                modification_date, 
                size, 
                file_hash, 
                code,
                status=Status.EVENT_TYPE_CREATED.value):
        
        self.name = name
        self.creation_date = creation_date
        self.path = path
        self.modification_date = modification_date
        self.size = size
        self.file_hash = file_hash
        self.code = code
        self.status = status


    @staticmethod
    def from_dict(data):
        return FilesModel(
            name=data.get('name'),
            creation_date=data.get('creation_date'),
            path=data.get('path'),
            modification_date=data.get('modification_date'),
            size=data.get('size'),
            file_hash=data.get('file_hash'),
            code=data.get('code'),
            status= Status(data.get('status')).value
        )


    def to_dict(self):
        return {
            'name': self.name,
            'creation_date': self.creation_date,
            'path': self.path,
            'modification_date': self.modification_date,
            'size': self.size,
            'file_hash': self.file_hash,
            'code': self.code,
            'status': self.status
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
        exclude_status: Optional[str] = None
    ) -> List['FilesModel']:
        '''
        Searches for all files of a `code` and excludes those with the `exclude_status`.
        
        :param code: The code of the file.
        :param exclude_status: The status to exclude (optional).
        :return: A list of `FilesModel` instances matching the criteria.
        '''

        query = {"code": code}
        if exclude_status is not None:
            query["status"] = {"$ne": exclude_status}  

        documents = cls.get_collection().find(query)
        files = []
        for document in documents:
            document['_id'] = str(document['_id'])
            files.append(document)

        return files