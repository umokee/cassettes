from collections.abc import Sequence

from data import Database
from data.entities import ClientStatus


class ClientStatusRepository:
    def __init__(self, db: Database):
        self._db = db

    def list(self) -> Sequence[ClientStatus]:
        sql = """
            SELECT
                id_client_status,
                name,
                description
            FROM client_status
            ORDER BY id_client_status;
        """
        rows = self._db.fetch_all(sql)
        return [ClientStatus.from_row(row) for row in rows]

    def get(self, id_client_status: int) -> ClientStatus | None:
        sql = """
            SELECT
                id_client_status,
                name,
                description
            FROM client_status
            WHERE id_client_status = %s;
        """
        row = self._db.fetch_one(sql, id_client_status)
        return ClientStatus.from_row(row) if row else None

    def add(self, name: str, description: str):
        sql = """
            INSERT INTO client_status (name, description)
            VALUES (%s, %s);
        """
        self._db.execute(sql, name, description)

    def delete(self, id_client_status: int):
        sql = """
            DELETE FROM client_status
            WHERE id_client_status = %s;
        """
        self._db.execute(sql, id_client_status)

    def update(self, id_client_status: int, name: str, desc: str):
        sql = """
            UPDATE client_status
            SET name = %s,
                description = %s
            WHERE id_client_status = %s;
        """
        self._db.execute(sql, name, desc, id_client_status)
