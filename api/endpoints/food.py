from typing import List

from ..http import HttpClient
from .. import config
from ..models.cafes import CampusCafes, CafeInfo, CafeMenu


class FoodAPI:
    def __init__(self, http: HttpClient):
        self.http = http

    def cafes(self) -> List[CampusCafes]:
        raw = self.http.get(config.url(config.API_DEFAULT_URL, "/food/cafes"))
        return [CampusCafes.model_validate(c) for c in raw]

    def cafe_info(self, cafe_id: str) -> CafeInfo:
        raw = self.http.get(config.url(config.API_DEFAULT_URL, f"/food/cafes/{cafe_id}"))
        return CafeInfo.model_validate(raw)

    def cafe_menu(self, cafe_id: str):
        raw = self.http.get(config.url(config.API_DEFAULT_URL, f"food/v2/cafes/{cafe_id}/menu"))
        return CafeMenu.model_validate(raw)
