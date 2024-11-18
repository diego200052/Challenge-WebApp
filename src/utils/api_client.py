import requests
from core.config import settings


class APIClient:
    def __init__(self, base_url=settings.API_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, params=None):
        response = self.session.get(f"{self.base_url}{endpoint}", params=params)
        return self.handle_response(response)

    def post(self, endpoint, data=None, json=None):
        response = self.session.post(f"{self.base_url}{endpoint}", data=data, json=json)
        return self.handle_response(response)

    def put(self, endpoint, data=None, json=None):
        response = self.session.put(f"{self.base_url}{endpoint}", data=data, json=json)
        return self.handle_response(response)

    def delete(self, endpoint):
        response = self.session.delete(f"{self.base_url}{endpoint}")
        return self.handle_response(response)

    @staticmethod
    def handle_response(response):
        if response.status_code not in [200, 201, 204]:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        return response.json() if response.content else None
