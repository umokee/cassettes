from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Employee:
    id_employee: int
    full_name: str
    login: str
    password: str
    email: str
    position: str

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "Employee":
        if len(row) == 6:
            return cls(*row)
        raise ValueError("Недопустимая строка для сотрудника")
