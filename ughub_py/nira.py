import requests
import json
import os
import base64
from typing import TypedDict
from typing import Dict

CredsDict = TypedDict("CredsDict",{"NIRA AUTH FORWARD":str,"CREATED DATE":str,"NONCE":str})


class Nira:
    def __init__(self):
        self.ughub_username = os.getenv("UGHUB_USERNAME")
        self.ughub_password = os.getenv("UGHUB_PASSWORD")
        self.username = os.getenv("NIRA_USERNAME")
        self.password = os.getenv("NIRA_PASSWORD")
        self.debug = os.getenv("DEBUG")
        self.host = "https://ughub.taufeeq.dev"

        if not self.debug:
            self.host = "https://ughub.taufeeq.dev"

        self._token = None

    def get_nira_token(self) -> str:
        url = f"{self.host}/token"
        payload = "grant_type=client_credentials"
        creds = base64.b64encode(
            f"{self.ughub_username}:{self.ughub_password}".encode("utf-8")
        ).decode("utf-8")
        headers = {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url, headers=headers, data=payload)
        res = response.json()
        access_token = res["access_token"]
        return access_token

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value

    def get_credentials(self) -> CredsDict:
        url = f"{self.host}/t/nira.go.ug/nitaauth/1.0.0/api/v1/access"
        payload = {
            "username": self.username,
            "password": self.password,
        }
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)
        res = response.json()
        return res

    def _generate_headers(self) -> Dict[str, str]:
        creds = self.get_credentials()
        nonce = creds["NONCE"]
        timestamp = creds["CREATED DATE"]
        nira_auth_forward = creds["NIRA AUTH FORWARD"]
        headers = {
            "Authorization": "Bearer " + self.token,
            "nira-auth-forward": nira_auth_forward,
            "nira-nonce": nonce,
            "nira-created": timestamp,
        }
        return headers

    def get_person(self, nin: str):
        self.token = self.get_nira_token()
        url = f"{self.host}/t/nira.go.ug/nira-api/1.0.0/getPerson?nationalId=" + nin
        headers = self._generate_headers()
        response = requests.get(url, headers=headers)
        return response

    def get_card(self, card_no: str):
        self.token = self.get_nira_token()
        url = f"{self.host}/t/nira.go.ug/nira-api/1.0.0/getIdCard?cardNumber={card_no}"
        headers = self._generate_headers()
        response = requests.get(url, headers=headers)
        return response
