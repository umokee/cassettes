from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(slots=True)
class PenaltyAccounting:
    id_fine: int
    id_rental: int
    accrual_date: date
    accrual_amount: float
    fine_reason: str | None = None

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "PenaltyAccounting":
        if len(row) == 4:
            return cls(*row)
        if len(row) == 5:
            id_fine, id_rental, accrual_date, accrual_amount, reason = row
            return cls(id_fine, id_rental, accrual_date, accrual_amount, reason)
        raise ValueError("Недопустимая строка для учета штрафов")
