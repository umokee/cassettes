from collections.abc import Sequence
from datetime import date

from data.entities import Fine, PenaltyAccounting, Rental
from data.repo import FineRepository, PenaltyAccountingRepository, RentalRepository


class PenaltyAccountingService:
    def __init__(
        self,
        repo: PenaltyAccountingRepository,
        fine_repo: FineRepository,
        rental_repo: RentalRepository,
    ):
        self._repo = repo
        self._fines = fine_repo
        self._rentals = rental_repo

    def list(self) -> Sequence[PenaltyAccounting]:
        return self._repo.get_all()

    def list_by_client(self, client_id: int) -> Sequence[PenaltyAccounting]:
        return self._repo.get_by_client(client_id)

    def get_fines(self) -> Sequence[Fine]:
        return self._fines.get_all()

    def get_rentals_for_client(self, client_id: int) -> Sequence[Rental]:
        return self._rentals.get_by_client(client_id)

    def accrue_fines(self, id_rental: int, fine_ids: Sequence[int]):
        if not fine_ids:
            raise ValueError("Не выбран ни один штраф")

        rental = self._rentals.get(id_rental)
        if rental is None:
            raise ValueError("Аренда не найдена")

        today = date.today()
        for fid in fine_ids:
            fine = self._fines.get(fid)
            if fine is None:
                raise ValueError("Штраф не найден")
            self._repo.add(fid, id_rental, today, fine.amount)
