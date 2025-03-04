from bson import ObjectId


class BaseModel:
    db = None
    
    def __init__(self):
        self._id = ''
        
    @classmethod
    def load(cls, db):
        cls.db = db

    @classmethod
    def get_collection_name(cls):
        return cls.__name__.lower()  # Ej: "Account" -> "accounts"

    @classmethod
    def get_collection(cls):
        return cls.db[cls.get_collection_name()]

    # @classmethod
    def save(self):
        '''Save the model to the database'''
        collection = self.__class__.get_collection()  
        print(f"COLLECTIO FROM: {self.__class__.__name__}")
        data = self.to_dict()  
        result = collection.insert_one(data)
        print(f'ID RESULT: {result.inserted_id}')
        self._id = result.inserted_id
        
        print(f"ID: {self._id}")
        return self._id

    @classmethod
    def find_by_id(cls, id):
        ''' Find the model by its id'''
        document = cls.get_collection().find_one({"_id": ObjectId(id)})
        if document:
            document['_id'] = str(document['_id'])
            return cls.from_dict(document)
        return None

    @classmethod
    def update(cls, id, update_data):
        '''Update the model with the new data'''
        result = cls.get_collection().update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    @classmethod
    def delete(cls, id):
        '''Deleting the model from the database'''
        result = cls.get_collection().delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    @staticmethod
    def from_dict(data):
        '''Convert a dictionary to a list of objects and return a list'''
        raise NotImplementedError("Subclasses must implement this method.")

    def to_dict(self):
        '''Convert a dictionary to a list of objects and return a list'''
        raise NotImplementedError("Subclasses must implement this method.")