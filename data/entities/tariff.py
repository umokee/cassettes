from dataclasses import dataclass
from typing import Any

from .tariff_condition import TariffCondition


@dataclass(slots=True)
class Tariff:
    id_tariff: int
    name: str
    coefficient: float
    provision_condition: TariffCondition
    type: str

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "Tariff":
        if len(row) == 5:
            id_tariff, name, coefficient, condition_json, type_name = row
            condition = TariffCondition.from_json(condition_json)
            return cls(id_tariff, name, coefficient, condition, type_name)
        raise ValueError("Недопустимая строка для тарифа")
