import requests
import json

class Nira:
    def __init__(self, base_url, auth_token, sandbox=False):
        self.base_url = base_url
        self.headers = self._generate_headers(auth_token)
        self.sandbox = sandbox

    def _generate_headers(self, auth_token):
        # Generate NIRA API headers using the auth token
        headers = {
            "Authorization": f"Bearer {auth_token}",
            # Add other required headers
        }
        return headers

    def _make_request(self, method, endpoint, params=None, payload=None):
        if self.sandbox:
            # Mock the response based on the endpoint
            response_data = self._mock_response(endpoint)
            return response_data

        url = self.base_url + endpoint
        response = requests.request(method, url, headers=self.headers, params=params, json=payload)

        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except json.JSONDecodeError:
                print("Error: Invalid JSON response.")
                return None
        else:
            print(f"Error: Request failed with status code {response.status_code}.")
            return None
        
    def get_person(self, person_id):
        # GET /getPerson
        endpoint = "/getPerson"
        params = {
            "personId": person_id
        }
        return self._make_request("GET", endpoint, params)
    
    def _mock_response(self, endpoint):
        # Implement logic to mock the response based on the endpoint
        # Return the mocked response data
        if endpoint == "/getPerson":
            mocked_data = {
                "name": "John Doe",
                "age": 30,
                # Add other mocked data fields
            }
            return mocked_data
        elif endpoint == "/getIdCard":
            # Mock response for getIdCard endpoint
            # ...
            pass
        elif endpoint == "/getPlaceOfResidence":
            # Mock response for getPlaceOfResidence endpoint
            # ...
            pass
        else:
            print("Error: No mocked response defined for the endpoint.")
            return None

    # ... other methods ...



