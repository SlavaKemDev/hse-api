from datetime import date
from typing import Optional, Dict, Any
from ..http import HttpClient
from .. import config
from ..models.timetable import Lesson


class RuzAPI:
    def __init__(self, http: HttpClient):
        self.http = http

    def lessons(self, email: str, start: date):
        raw = self.http.get(
            config.url(config.API_V3_URL, "ruz/lessons"),
            params={"email": email, "start": start.strftime("%Y-%m-%d")}
        )

        return [Lesson.model_validate(item) for item in raw]
