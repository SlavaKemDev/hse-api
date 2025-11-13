from datetime import date
from typing import Optional
from .auth import password_grant, refresh_grant
from .http import HttpClient
from .endpoints.ruz import RuzAPI
from .endpoints.grades import GradesAPI
from .endpoints.food import FoodAPI


class Account:
    def __init__(self, email: str, access_token: str, refresh_token: str):
        self.email = email
        self._refresh_token = refresh_token

        def _refresh():
            new_access = refresh_grant(self._refresh_token)
            return new_access

        self._http = HttpClient(access_token=access_token, refresh_fn=_refresh)
        self.ruz = RuzAPI(self._http)
        self._grades = GradesAPI(self._http)
        self._food = FoodAPI(self._http)

    @staticmethod
    def auth(email: str, password: str) -> "Account":
        access, refresh = password_grant(email, password)
        return Account(email=email, access_token=access, refresh_token=refresh)

    def get_timetable(self, email: Optional[str] = None, start_date: Optional[date] = None):
        return self.ruz.lessons(email or self.email, start_date or date.today())

    def get_grades(self, academic_year: Optional[str] = None, program_id: Optional[int] = None):
        return self._grades.grades(academic_year, program_id)

    def get_cafes(self):
        return self._food.cafes()

    def get_cafe_info(self, cafe_id: str):
        return self._food.cafe_info(cafe_id)

    def get_cafe_menu(self, cafe_id: str):
        return self._food.cafe_menu(cafe_id)
