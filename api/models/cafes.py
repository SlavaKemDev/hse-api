from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Coordinates(BaseModel):
    lat: float
    lng: float


class OpeningHours(BaseModel):
    day_of_week: str
    is_open: bool
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    class Config:
        extra = "ignore"


class Navigation(BaseModel):
    room: int | str  # API может возвращать как int, так и str
    floor: int

    class Config:
        extra = "ignore"


class Cafe(BaseModel):
    cafe_id: str
    cafe_name: str

    opening_hours: List[OpeningHours]

    closed_dates: Optional[List[str]] = None
    address: str
    coordinates: Coordinates

    has_menu: bool = False

    photos: Optional[List[str]] = None
    photo: Optional[str] = None

    description: Optional[str] = None
    banner: Optional[str] = None

    navigation: Optional[Navigation] = None

    class Config:
        extra = "ignore"


class CafeInfo(Cafe):
    """
    Детальная инфа по одной точке.
    Сейчас совпадает с Cafe, но отдельная модель удобна
    как "семантический" тип для get_cafe_info().
    """
    pass


class CampusCafes(BaseModel):
    cafes: List[Cafe]

    campus_id: str
    campus_name: str
    coordinates: Coordinates

    class Config:
        extra = "ignore"


# ====== МЕНЮ КАФЕ ======

class MenuProp(BaseModel):
    type: str
    value: str
    label: str

    class Config:
        extra = "ignore"


class MenuItem(BaseModel):
    item_name: str
    item_name_opt: Optional[str] = None
    item_id: str

    price: Optional[int] = None

    props: List[MenuProp] = []
    composition: Optional[str] = None
    chips: Optional[List[str]] = None
    section: str

    class Config:
        extra = "ignore"


class MenuSection(BaseModel):
    section_name: str
    section: str
    items: List[MenuItem]
    price: Optional[int] = None  # для комплексов

    class Config:
        extra = "ignore"


class CafeMenu(BaseModel):
    cafe_id: str
    current_day: str
    available_days: List[str]
    sections: List[MenuSection]

    class Config:
        extra = "ignore"
