from __future__ import annotations

import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class GradeValue(BaseModel):
    ten_point_scale: int
    five_point_scale: int
    pass_: bool = Field(alias="pass")  # pass is a reserved keyword in Python

    class Config:
        populate_by_name = True  # Обновлено для Pydantic V2
        extra = "ignore"


class GradeItem(BaseModel):
    student_status_hr_uid: str
    asav_uid: Optional[str] = None
    hr_uid: str

    module_num: str  # "1", "2", ...
    academic_year: str  # "2025/2026"
    id: str
    program_id: str
    discipline: str
    type_raw: str  # "Экзамен", "Зачет", ...

    repass_count: int

    grade: Optional[GradeValue] = None
    date: Union[datetime.date, None] = None

    module_name: str  # "1 модуль"
    period_credits: int
    credits: int
    entire_hours: int
    aud_hours: int

    lecturer: Optional[str] = None

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        """Преобразует строку даты в объект date"""
        if v is None or isinstance(v, datetime.date):
            return v
        if isinstance(v, str):
            return datetime.date.fromisoformat(v)
        return v

    class Config:
        extra = "ignore"


class ProgramInfo(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

    class Config:
        extra = "ignore"


class GradesResponse(BaseModel):
    items: List[GradeItem]

    available_academic_years: List[str]
    selected_academic_year: str
    selected_program: str
    available_programs: List[ProgramInfo]
    current_academic_year: str

    class Config:
        extra = "ignore"
