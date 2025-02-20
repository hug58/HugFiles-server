from typing import List
import json


class BasicDb:
    """
    SAVE JSON IN FILES.
    """

    @staticmethod
    def initialize_file(file_path):
        """
        Creates the JSON file if it does not exist, initializing it with an empty object.
        """
        try:
            with open(file_path, 'x') as file:
                json.dump({}, file)
        except FileExistsError:
            pass  # Do nothing if the file already exists.

    @staticmethod
    def _load_data(file_path:str) -> dict:
        """
        Loads data from the JSON file.
        :return: Dictionary with the loaded data.
        """
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def _save_data(file_path:str, data: dict):
        """
        Saves the data to the JSON file.
        :param data: Dictionary containing the data to save.
        """
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def save(file_path:str, collection: str, data: dict) -> dict:
        """
        Saves a document to the specified collection.
        :param collection: Name of the collection (key in the JSON).
        :param data: Document (dictionary) to save.
        :return: The saved document.
        """
        db = BasicDb._load_data(file_path=file_path)
        if collection not in db:
            db[collection] = []
        db[collection].append(data)
        BasicDb._save_data(file_path,db)
        return data

    @staticmethod
    def update(file_path:str, collection: str, query: dict, new_data: dict) -> List[dict]:
        """
        Updates one or more documents in the JSON file based on a query.

        :param collection: Name of the collection (key in the JSON).
        :param query: Dictionary representing the search criteria.
        :param new_data: Dictionary with the new data to update.
        :return: List of updated documents or an empty list if no matches were found.
        """

        db = BasicDb._load_data(file_path=file_path)
        updated_items = []

        if collection in db:
            for item in db[collection]:
                if all(item.get(k) == v for k, v in query.items()):
                    item.update(new_data)
                    updated_items.append(item)

            if updated_items:
                BasicDb._save_data(file_path, db)

        return updated_items

    @staticmethod
    def find(file_path:str, collection: str, query: dict) -> List[dict]:
        """
        Searches for documents in the collection that match the query.
        :param collection: Name of the collection.
        :param query: Dictionary representing the search criteria.
        :return: List of matching documents.
        """
        db = BasicDb._load_data(file_path=file_path)
        if collection not in db:
            return []
        return [item for item in db[collection] if all(item.get(k) == v for k, v in query.items())]

