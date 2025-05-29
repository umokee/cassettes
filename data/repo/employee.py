from collections.abc import Sequence

from data import Database
from data.entities import Employee


class EmployeeRepository:
    def __init__(self, db: Database):
        self._db = db

    def auth(self, login: str, password: str) -> Employee | None:
        sql = """
            SELECT
                e.id_employee,
                e.full_name,
                e.login,
                e.password,
                e.email,
                p.name
            FROM employee e
            JOIN position p
                ON e.id_position = p.id_position
            WHERE e.login = %s AND e.password = %s;
        """
        row = self._db.fetch_one(sql, login, password)
        return Employee.from_row(row) if row else None

    def list(self) -> Sequence[Employee]:
        sql = """
            SELECT
                e.id_employee,
                e.full_name,
                e.login,
                e.password,
                e.email,
                p.name
            FROM employee e
            JOIN position p
                ON e.id_position = p.id_position
            ORDER BY id_employee;
        """
        rows = self._db.fetch_all(sql)
        return [Employee.from_row(row) for row in rows]

    def get(self, id_employee: int) -> Employee | None:
        sql = """
            SELECT
                e.id_employee,
                e.full_name,
                e.login,
                e.password,
                e.email,
                p.name
            FROM employee e
            JOIN position p
                ON e.id_position = p.id_position
            WHERE id_employee = %s;
        """
        row = self._db.fetch_one(sql, id_employee)
        return Employee.from_row(row) if row else None

    def add(self, full_name: str, login: str, password: str, email: str, id_position: int):
        sql = """
            INSERT INTO employee (full_name, login, password, email, id_position)
            VALUES (%s, %s, %s, %s, %s);
        """
        self._db.execute(sql, full_name, login, password, email, id_position)

    def update(
        self,
        id_employee: int,
        full_name: str,
        login: str,
        password: str,
        email: str,
        id_position: int,
    ):
        sql = """
            UPDATE employee
            SET full_name = %s,
                login = %s,
                password = %s,
                email = %s,
                id_position = %s
            WHERE id_employee = %s;
        """
        self._db.execute(sql, full_name, login, password, email, id_position, id_employee)
