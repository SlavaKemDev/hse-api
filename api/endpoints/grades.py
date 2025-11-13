from typing import Optional, Dict, Any
from ..http import HttpClient
from .. import config


class GradesAPI:
    def __init__(self, http: HttpClient):
        self.http = http

    def grades(self, academic_year: Optional[str] = None, program_id: Optional[int] = None):
        params: Dict[str, Any] = {}

        if academic_year:
            params["academic_year"] = academic_year

        if program_id:
            params["program_id"] = program_id

        return self.http.get(config.url(config.API_V2_URL, "grades"), params=params)
