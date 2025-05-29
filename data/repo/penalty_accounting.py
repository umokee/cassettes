from collections.abc import Sequence
from datetime import date

from data import Database
from data.entities import PenaltyAccounting


class PenaltyAccountingRepository:
    def __init__(self, db: Database):
        self._db = db

    def get_all(self) -> Sequence[PenaltyAccounting]:
        sql = """
            SELECT
                pa.fine_id_fine,
                pa.rental_id_rental,
                pa.accrual_date,
                pa.accrual_amount,
                f.reason
            FROM penalty_accounting pa
            JOIN fine f ON f.id_fine = pa.fine_id_fine
            ORDER BY pa.accrual_date DESC;
        """
        rows = self._db.fetch_all(sql)
        return [PenaltyAccounting.from_row(row) for row in rows]

    def get_by_client(self, id_client: int) -> Sequence[PenaltyAccounting]:
        sql = """
            SELECT
                pa.fine_id_fine,
                pa.rental_id_rental,
                pa.accrual_date,
                pa.accrual_amount,
                f.reason
            FROM penalty_accounting pa
            JOIN rental r
                ON r.id_rental = pa.rental_id_rental
            JOIN fine f
                ON f.id_fine = pa.fine_id_fine
            WHERE r.id_client = %s
            ORDER BY pa.accrual_date DESC;
        """
        rows = self._db.fetch_all(sql, id_client)
        return [PenaltyAccounting.from_row(row) for row in rows]

    def add(self, id_fine: int, id_rental: int, accrual_date: date, amount: float) -> None:
        sql = """
            INSERT INTO penalty_accounting (
                fine_id_fine,
                rental_id_rental,
                accrual_date,
                accrual_amount
            ) VALUES (%s, %s, %s, %s);
        """
        self._db.execute(sql, id_fine, id_rental, accrual_date, amount)
