from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Fine:
    id_fine: int
    reason: str
    amount: float

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "Fine":
        if len(row) == 3:
            return cls(*row)
        raise ValueError("Недопустимая строка для штрафа")
