from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(slots=True)
class Rental:
    id_rental: int
    id_client: int
    id_cassette: int
    id_employee_take: int
    id_employee_give: int | None
    rental_date: date
    rental_duration: int
    return_date: date | None
    rental_cost: float
    cassette_condition_after: str | None
    status: str

    @classmethod
    def new(
        cls, id_client: int, id_cassette: int, id_employee: int, duration: int, cost: float
    ) -> "Rental":
        return cls(
            id_rental=0,
            id_client=id_client,
            id_cassette=id_cassette,
            id_employee_take=id_employee,
            id_employee_give=None,
            rental_date=date.today(),
            rental_duration=duration,
            return_date=None,
            rental_cost=cost,
            cassette_condition_after=None,
            status="В процессе",
        )

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "Rental":
        if len(row) == 11:
            return cls(*row)
        raise ValueError("row size mismatch for Rental")
