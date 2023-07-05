import base64
import requests
import os

class URSBClient:
    def __init__(self):
        self.consumerKey = os.getenv("URSB_CONSUMER_KEY")
        self.consumerSecret = os.getenv("URSB_CONSUMER_SECRET")
        self.ursb_key = os.getenv("URSB_KEY")
        
        self.debug = os.getenv("DEBUG")
        self.host = "https://api-uat.integration.go.ug"
        

        if not self.debug:
            self.host = "https://api-uat.integration.go.ug"

        self._token = None

    
    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self,value:str):
        self._token = value
    
    
    def generateAccessToken(self)->str:
        # Encode the consumer key and consumer secret in base64
        credentials = f"{self.consumerKey}:{self.consumerSecret}"
        base64EncodedCredentials = base64.b64encode(credentials.encode()).decode()

        # Send the request to obtain the access token
        response = requests.post(
            f"{self.host}/token",
            headers={"Authorization": f"Basic {base64EncodedCredentials}"},
            data={"grant_type": "client_credentials"}
        )
        accessToken = response.json()["access_token"]
        
        return accessToken
    
    def invokeAPIResource(self, resourcePath):
        # Send the request to invoke the API resource
        headers = {"Authorization": f"Bearer {self.token}"}
        print(headers)
        response = requests.get(f"{self.host}{resourcePath}", headers=headers)
        
        statusCode = response.status_code
        if 400 <= statusCode < 500:
            raise Exception(f"Client error: {statusCode}")
        
        if 500 <= statusCode < 600:
            raise Exception(f"Server error: {statusCode}")
        
        return response.text
    
    def find(self, id):
        self.token = self.generateAccessToken()
        # Generic method
        resourcePath = f"/t/ursb.go.ug/ursb-brs-api/1.0.0/entity/get_entity_full/{id}/-/{self.ursb_key}"
        return self.invokeAPIResource(resourcePath)
