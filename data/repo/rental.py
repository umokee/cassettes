from collections.abc import Sequence
from datetime import date

from data import Database
from data.entities import Rental


class RentalRepository:
    def __init__(self, db: Database):
        self._db = db

    def list_open(self) -> Sequence[Rental]:
        sql = """
            SELECT * FROM rental
            WHERE rental_status = 'В процессе'
            ORDER BY id_rental
        """
        return [Rental.from_row(r) for r in self._db.fetch_all(sql)]

    def list_all(self) -> Sequence[Rental]:
        sql = """
            SELECT * FROM rental
            ORDER BY id_rental DESC
        """
        return [Rental.from_row(r) for r in self._db.fetch_all(sql)]

    def get(self, id_rental: int) -> Rental | None:
        sql = """
            SELECT * FROM rental
            WHERE id_rental=%s
        """
        row = self._db.fetch_one(sql, id_rental)
        return Rental.from_row(row) if row else None

    def add(self, r: Rental) -> int:
        sql = """
            INSERT INTO rental (
                client_id_client, cassette_id_cassette,
                employee_id_employee_take, rental_date, rental_duration,
                rental_cost, rental_status
            )
            VALUES (%s,%s,%s,%s,%s,%s,'В процессе')
            RETURNING id_rental
        """
        row = self._db.fetch_one(
            sql,
            r.id_client,
            r.id_cassette,
            r.id_employee_take,
            r.rental_date,
            r.rental_duration,
            r.rental_cost,
        )
        return int(row[0])

    def close(
        self,
        id_rental: int,
        id_emp_return: int,
        return_date: date,
        cassette_cond_after: str,
    ) -> None:
        sql = """
            UPDATE rental
            SET employee_id_employee_give=%s,
                return_date=%s,
                cassette_condition_after_rental=%s,
                rental_status='Завершено'
            WHERE id_rental=%s
        """
        self._db.execute(sql, id_emp_return, return_date, cassette_cond_after, id_rental)

        sql = """
            UPDATE cassette
            SET condition=%s
            WHERE id_cassette = (
                SELECT id_cassette
                FROM rental
                WHERE id_rental=%s
            )
        """
        self._db.execute(sql, cassette_cond_after, id_rental)
