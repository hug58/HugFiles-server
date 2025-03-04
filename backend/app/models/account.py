from .base_model import BaseModel

class Accounts(BaseModel):
    def __init__(self, username, code, files=[]):
        self.username = username
        self.code = code
        self.files:list = files

    @staticmethod
    def from_dict(data):
        return Accounts(
            username=data.get('username'),
            code=data.get('code'),
            files=data.get('files', [])
        )

    def to_dict(self):
        return {
            'username': self.username,
            'code': self.code,
            'files': self.files
        }

    @classmethod
    def find_by_username(cls, username) -> dict:
        ''' Find the model by its username'''
        document = cls.get_collection().find_one({"username": username})
        if document:
            document['_id'] = str(document['_id'])
            return cls.from_dict(document)
        return None

    @classmethod
    def find_by_code(cls, code):
        ''' Find the model by its code'''
        document = cls.get_collection().find_one({"code": code})
        if document:
            document['_id'] = str(document['_id'])
            return cls.from_dict(document)
        return None
    
    
    @classmethod
    def update_files(cls, code, new_files):
        '''Update the files array for the account with the given code'''
        result = cls.get_collection().update_one(
            {"code": code},
            {"$set": {"files": new_files}}
        )
        return result.modified_count > 0