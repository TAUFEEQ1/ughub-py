import requests
import json
import os
import base64
from typing import TypedDict

CredsDict = TypedDict("CredsDict",{"NIRA AUTH FORWARD":str,"CREATED DATE":str,"NONCE":str})
    
class Nira:
    ughub_username = os.getenv("UGHUB_USERNAME")
    ughub_password = os.getenv("UGHUB_PASSWORD")
    
    username = os.getenv("NIRA_USERNAME")
    password = os.getenv("NIRA_PASSWORD") 
    
    debug = os.getenv("DEBUG")
    
    host = "https://ughub.taufeeq.dev"
    
    def __init__(self) -> None:
        if not self.debug:    
            self.host = "https://ughub.taufeeq.dev"
    
    def get_nira_token(self)->str:
        url = f'{self.host}/token'
        payload = 'grant_type=client_credentials'
        creds = base64.b64encode(f"{self.ughub_username}:{self.ughub_password}".encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {creds}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload)
        res = response.json()
        access_token = res['access_token']
        return access_token
    
    def get_credentials(self)->CredsDict:
        token = self.get_nira_token()
        url = f'{self.host}/t/nira.go.ug/nitaauth/1.0.0/api/v1/access'
        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=payload)
        res = response.json()
        return res
    
    def _generate_headers(self):
        creds = self.get_credentials()
        token = self.get_nira_token()
        nonce = creds['NONCE']
        timestamp = creds['CREATED DATE']
        nira_auth_forward = creds['NIRA AUTH FORWARD'] 
        # Generate NIRA API headers using the auth token
        headers = {
            'Authorization': 'Bearer ' + token,
            'nira-auth-forward': nira_auth_forward,
            'nira-nonce': nonce,
            'nira-created': timestamp
        }
        return headers
        
    
    def get_person(self,nin:str):
        url = f'{self.host}/t/nira.go.ug/nira-api/1.0.0/getPerson?nationalId=' + nin
        response = requests.get(url, headers=self._generate_headers())
        return response
    
    
    
    
    