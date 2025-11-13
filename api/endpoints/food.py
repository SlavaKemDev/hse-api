from ..http import HttpClient
from .. import config


class FoodAPI:
    def __init__(self, http: HttpClient):
        self.http = http

    def cafes(self):
        return self.http.get(config.url(config.API_DEFAULT_URL, "food/cafes"))

    def cafe_info(self, cafe_id: str):
        return self.http.get(config.url(config.API_DEFAULT_URL, f"food/cafes/{cafe_id}"))

    def cafe_menu(self, cafe_id: str):
        return self.http.get(config.url(config.API_DEFAULT_URL, f"food/v2/cafes/{cafe_id}/menu"))
