from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class GeoPoint(BaseModel):
    type: str
    coordinates: List[float]  # [longitude, latitude]

    class Config:
        extra = "ignore"


class LecturerProfile(BaseModel):
    id: str
    full_name: str
    email: str
    avatar_url: Optional[str] = None
    description: Optional[str] = None
    has_phone: Optional[bool] = None  # может отсутствовать в некоторых ответах
    type: Optional[str] = None  # может отсутствовать в некоторых ответах

    class Config:
        extra = "ignore"


class StreamLink(BaseModel):
    link: str
    description: Optional[str] = None

    class Config:
        extra = "ignore"


class Lesson(BaseModel):
    id: str
    type: str  # "Лекция", "Проведение семинаров (студенты)", ...
    stream: str
    city: str

    # аудитория / кампус
    auditorium_id: Optional[int] = None
    auditorium: str
    building_id: Optional[int] = None
    building: Optional[str] = None
    location: Optional[GeoPoint] = None

    # дисциплина
    discipline: str
    discipline_link: Optional[str] = None
    kindOfWork: str  # дублирует type, idk

    # время
    date_start: datetime
    date_end: datetime
    created_at: datetime
    updated_at: datetime
    lesson_number_start: int
    lesson_number_end: int
    duration: List[int]  # иногда несколько пар подряд (например, когда коллоквиум)

    # преподаватели
    lecturer_emails: Optional[List[str]] = None
    lecturer_profiles: List[LecturerProfile] = []

    # заметки и ссылки
    note: Optional[str] = None
    stream_links: Optional[List[StreamLink]] = None

    # прочее
    importance_level: int
    hash: str

    class Config:
        extra = "ignore"
