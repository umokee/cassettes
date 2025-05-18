from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Cassette:
    id_cassette: int
    title: str
    condition: str
    rental_cost: float
    genres: str = ""
    genre_ids: Sequence[int] = ()

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "Cassette":
        if len(row) == 5:
            return cls(*row, genre_ids=())
        raise ValueError("Недопустимая строка для кассеты")
