from collections.abc import Sequence
from datetime import date

from data.entities import Cassette, Rental, Tariff
from data.repo import RentalRepository


class RentalService:
    def __init__(self, repo: RentalRepository):
        self._repo = repo

    def get_active(self) -> Sequence[Rental]:
        return self._repo.get_active()

    def get(self, id_rental: int) -> Rental | None:
        return self._repo.get(id_rental)

    def get_by_client(self, id_client: int) -> Sequence[Rental]:
        return self._repo.get_by_client(id_client)

    def calc_cost(self, cassette: Cassette, tarriff: Tariff, days: int) -> float:
        return cassette.rental_cost * tarriff.coefficient * days

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
    ):
        self._repo.close(id_rental, id_employee_give, date.today(), cassette_cond_after)
