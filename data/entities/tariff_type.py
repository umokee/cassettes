from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class TariffType:
    id_tariff_type: int
    name: str
    description: str

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "TariffType":
        if len(row) == 3:
            return cls(*row)
        raise ValueError("Недопустимая строка для типа тарифа")
