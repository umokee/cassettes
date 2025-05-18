from collections.abc import Sequence

from data import Database
from data.entities import Client


class ClientRepository:
    def __init__(self, db: Database):
        self._db = db

    def list(self) -> Sequence[Client]:
        sql = """
            SELECT c.id_client, c.full_name, c.login, c.password, c.email, cs.name
            FROM client c
            JOIN client_status cs ON c.id_client_status=cs.id_client_status
            ORDER BY id_client;
        """
        rows = self._db.fetch_all(sql)
        return [Client.from_row(row) for row in rows]

    def get(self, id_client: int) -> Client | None:
        sql = """
            SELECT c.id_client, c.full_name, c.login, c.password, c.email, cs.name
            FROM client c
            JOIN client_status cs ON c.id_client_status=cs.id_client_status
            WHERE id_client=%s;
        """
        row = self._db.fetch_one(sql, id_client)
        return Client.from_row(row) if row else None

    def add(self, full_name: str, login: str, email: str, id_status: int):
        sql = """
            INSERT INTO client (full_name, login, email, id_client_status)
            VALUES (%s, %s, %s, %s);
        """
        self._db.execute(sql, full_name, login, email, id_status)

    def update(self, id_client: int, full_name: str, login: str, email: str, id_status: int):
        sql = """
            UPDATE client
            SET full_name=%s, login=%s, email=%s, id_client_status=%s
            WHERE id_client=%s;
        """
        self._db.execute(sql, full_name, login, email, id_status, id_client)

    def update_password(self, id_client: int, new_password: str):
        sql = """
            UPDATE client
            SET password = %s
            WHERE id_client = %s
        """
        self._db.execute(sql, new_password, id_client)
