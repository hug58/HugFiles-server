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
    
    @staticmethod
    def send(flags="GET",message={}):
        """Send data to server"""
        if flags == "POST":
            response = requests.post(message['url'], files = {'upload_file': open(message['path'],'rb')},timeout=100)
            if response.status_code == 200:
                return response.json()
            
        elif flags == "PUT":
            response = requests.put(urljoin(message['url'],message['name']), files = {'upload_file': open(message['path'],'rb')},
                timeout=100,
                headers={'Content-Type': 'application/json'})
        
        elif flags == "DELETE":
            response = requests.delete(urljoin(message['url'],message['name']),
                timeout=100,
                headers={'Content-Type': 'application/json'})       



        return None
