from data import Database
from data.entities import Employee


class EmployeeRepository:
    def __init__(self, db: Database):
        self._db = db

    def auth(self, login: str, password: str) -> Employee | None:
        sql = """
            SELECT e.id_employee, e.full_name, e.login, e.password, e.email, p.name
            FROM employee e
            JOIN position p ON e.id_position=p.id_position
            WHERE e.login=%s AND e.password=%s;
        """
        row = self._db.fetch_one(sql, login, password)
        return Employee.from_row(row) if row else None
