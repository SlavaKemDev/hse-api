from typing import Optional

import requests
from datetime import datetime, date
from urllib.parse import urljoin
from dotenv import load_dotenv
import os

load_dotenv()


class Account:
    V2_API_ENDPOINT = "https://api.hseapp.ru/v2/"
    V3_API_ENDPOINT = "https://api.hseapp.ru/v3/"
    API_ENDPOINT = "https://api.hseapp.ru/"

    def __init__(self, email, access_token, refresh_token):
        self.email = email
        self.access_token = access_token
        self.refresh_token = refresh_token

    def _query_get(self, endpoint, params=None):
        response = requests.get(endpoint, headers={
            "Authorization": f"Bearer {self.access_token}"
        }, params=params)

        return response.json()

    def _query_post(self, endpoint, params=None):
        response = requests.post(endpoint, headers={
            "Authorization": f"Bearer {self.access_token}"
        }, data=params)

        return response.json()

    def get_timetable(self, email: Optional[str] = None, start_date: Optional[date] = None):
        if not email:
            email = self.email
        if not start_date:
            start_date = date.today()

        return requests.get(urljoin(self.V3_API_ENDPOINT, "ruz/lessons"), params={
            "email": email,
            "start": start_date.strftime("%Y-%m-%d")
        }).json()

    def get_grades(self, academic_year: Optional[str] = None, program_id: Optional[int] = None):
        params = {}
        if academic_year:
            params["academic_year"] = academic_year
        if program_id:
            params["program_id"] = program_id
        return self._query_get(urljoin(self.V2_API_ENDPOINT, "grades"), params)

    def get_cafes(self):
        return self._query_get(urljoin(self.API_ENDPOINT, "food/cafes"))

    def get_cafe_info(self, cafe_id: str):
        return self._query_get(urljoin(self.API_ENDPOINT, f"food/cafes/{cafe_id}"))

    def get_cafe_menu(self, cafe_id: str):
        return self._query_get(urljoin(self.API_ENDPOINT, f"food/v2/cafes/{cafe_id}/menu"))

    @staticmethod
    def auth(email, password):
        # {
        #     "access_token": JWT,
        #     "expires_in": 10800,
        #     "refresh_expires_in": 1814400,
        #     "refresh_token": JWT,
        #     "token_type": "Bearer",
        #     "not-before-policy": 0,
        #     "session_state": UUID,
        #     "scope": "profile email"
        # }

        query = requests.post("https://saml.hse.ru/realms/hse/protocol/openid-connect/token", data={
            "client_id": "app-x-ios",
            "username": email,
            "password": password,
            "grant_type": "password"
        })

        if query.status_code != 200:
            raise Exception("Invalid credentials")

        response = query.json()

        return Account(
            email=email,
            access_token=response["access_token"],
            refresh_token=response["refresh_token"]
        )


account = Account.auth(os.environ['email'], os.environ['password'])
print(account.get_timetable())
print(account.get_grades())
print(account.get_cafes())
print(account.get_cafe_info("64ed04c9411dc0b2e4890e42"))
print(account.get_cafe_menu("64ed04c9411dc0b2e4890e42"))

