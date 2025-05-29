from collections.abc import Sequence
from datetime import date

from data import Database
from data.entities import Rental


class RentalRepository:
    def __init__(self, db: Database):
        self._db = db

    def get_active(self) -> Sequence[Rental]:
        sql = """
            SELECT
                id_rental,
                id_client,
                id_cassette,
                id_employee_take,
                id_employee_give,
                rental_date,
                rental_duration,
                return_date,
                rental_cost,
                cassette_condition_after,
                status
            FROM rental
            WHERE status = 'В процессе'
            ORDER BY id_rental;
        """
        rows = self._db.fetch_all(sql)
        return [Rental.from_row(row) for row in rows]

    def get(self, id_rental: int) -> Rental | None:
        sql = """
            SELECT
                id_rental,
                id_client,
                id_cassette,
                id_employee_take,
                id_employee_give,
                rental_date,
                rental_duration,
                return_date,
                rental_cost,
                cassette_condition_after,
                status
            FROM rental
            WHERE id_rental = %s;
        """
        row = self._db.fetch_one(sql, id_rental)
        return Rental.from_row(row) if row else None

    def get_by_client(self, id_client: int) -> Rental | None:
        sql = """
            SELECT
                id_rental,
                id_client,
                id_cassette,
                id_employee_take,
                id_employee_give,
                rental_date,
                rental_duration,
                return_date,
                rental_cost,
                cassette_condition_after,
                status
            FROM rental
            WHERE id_client = %s
            ORDER BY rental_date DESC;
        """
        rows = self._db.fetch_all(sql, id_client)
        return [Rental.from_row(row) for row in rows]

    def add(self, r: Rental) -> int:
        sql = """
            INSERT INTO rental (id_client,
                                id_cassette,
                                id_employee_take,
                                rental_date,
                                rental_duration,
                                rental_cost,
                                status)
            VALUES (%s, %s, %s, %s, %s, %s, 'В процессе')
            RETURNING id_rental;
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
    ):
        sql = """
            UPDATE rental
            SET id_employee_give = %s,
                return_date = %s,
                cassette_condition_after = %s,
                status = 'Завершено'
            WHERE id_rental = %s;
        """
        self._db.execute(sql, id_emp_return, return_date, cassette_cond_after, id_rental)

        sql = """
            UPDATE cassette
            SET condition = %s
            WHERE id_cassette = (
                SELECT id_cassette
                FROM rental
                WHERE id_rental = %s
            );
        """
        self._db.execute(sql, cassette_cond_after, id_rental)
