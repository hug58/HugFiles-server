import os
from plyer import notification
from colorama import init, Fore

from utils import get_config, set_email, set_folder
from .api import Api

class TerminalInterface:
    def __init__(self, default=None, user=None):
        self._email = user
        self._path = default
        self._connected = False
        self._code = None
        init()


    def submit_email(self):
        ''' get email if config not available. '''
        color = Fore.RED
        
        while self._email is None:
            email = input('Input email: ')
            if email and  len(email) > 0 :
                self._email = email
                set_email(self._email)
                break
            print(f'{color}Please select a valid email {color}█{Fore.RESET}')

    def select_folder(self):
        color = Fore.RED
        while self._path is None:
            folder_path = input('Select Directory: ')
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                self._path = folder_path
                set_folder(self._path)
                break
            
            print(f'{color}Please select a folder that exists {color}█{Fore.RESET}')
        
        
    def toggle_connection(self):
        self._connected = not self._connected
        self.draw_connection_circle()


    def draw_connection_circle(self):
        color = Fore.GREEN if self._connected else Fore.RED
        print(f'{color} Connection Status: {color}█{Fore.RESET}')
        
    
    @staticmethod
    def on():
        return Fore.BLUE
        
        
    def loop(self):
        self.draw_connection_circle()
        
        
        while not self._email or not self._path:
            
            self.select_folder()
            self.submit_email()
            
            if self._path != None and self._email != None:
                self.toggle_connection()
                break
        
        self._code = Api.get_token(self._email)
        
        notification.notify(
            title='Login Success',
            message=f'User {self._email} has successfully registered. code: {self._code}',
            app_name='HugoFiles-client',
            timeout=10  # Duración en segundos que la notificación estará visible
        )
        
        if not self._code:
            print('failed to get token...')
        self.toggle_connection()

                
    @property
    def email(self):
        return self._email
    
    
    @property
    def path(self):
        return self._path
    
    
    @property
    def code(self):
        return self._code

