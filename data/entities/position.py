from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Position:
    id_position: int
    name: str
    description: str

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "Position":
        if len(row) == 3:
            return cls(*row)
        raise ValueError("Недопустимая строка для должности")
