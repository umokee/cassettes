from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Genre:
    id_genre: int
    name: str
    description: str

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "Genre":
        if len(row) == 3:
            return cls(*row)
        raise ValueError("Недопустимая строка для жанра")
