import requests
import json
from urllib.parse import urljoin


class Api:
    """Login and access"""
    def __init__(self, url):
        self.url = url

    def get_token(self, email:str) -> str:
        """ create and login user in database[dirs]"""
        url = urljoin(self.url, "/token")
        response = requests.post(url, json={"email": email}, 
                                 headers={'Content-Type': 'application/json'},timeout=10)
        if response.status_code == 200:
            code = response.json()["code"]
            print(f"loggin with code: {code}")
            return code
        return ""
