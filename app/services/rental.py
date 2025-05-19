from collections.abc import Sequence
from datetime import date

from data.entities import Rental
from data.repo import RentalRepository


class RentalService:
    """Минималистичный сервис: CRUD + смена статуса."""

    def __init__(self, repo: RentalRepository):
        self._repo = repo

    # ---------- read ----------
    def list_open(self) -> Sequence[Rental]:
        return self._repo.list_open()

    def get(self, id_rental: int) -> Rental | None:
        return self._repo.get(id_rental)

    # ---------- write ----------
    def open_rental(
        self,
        id_client: int,
        id_cassette: int,
        id_employee_take: int,
        duration: int,
        cost: float,
    ) -> int:
        r = Rental.new(id_client, id_cassette, id_employee_take, duration, cost)
        return self._repo.add(r)

    def close_rental(
        self,
        id_rental: int,
        id_employee_give: int,
        cassette_cond_after: str,
    ) -> None:
        self._repo.close(id_rental, id_employee_give, date.today(), cassette_cond_after)
