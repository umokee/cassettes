from collections.abc import Sequence

from data import Database
from data.entities import Fine


class FineRepository:
    def __init__(self, db: Database):
        self._db = db

    def list(self) -> Sequence[Fine]:
        sql = """
            SELECT id_fine, reason, amount
            FROM fine
            ORDER BY id_fine;
        """
        rows = self._db.fetch_all(sql)
        return [Fine.from_row(row) for row in rows]

    def get(self, id_fine: int) -> Fine | None:
        sql = """
            SELECT id_fine, reason, amount
            FROM fine
            WHERE id_fine=%s;
        """
        row = self._db.fetch_one(sql, id_fine)
        return Fine.from_row(row) if row else None

    def add(self, reason: str, amount: float):
        sql = """
            INSERT INTO fine (reason, amount)
            VALUES (%s, %s);
        """
        self._db.execute(sql, reason, amount)

    def delete(self, id_fine: int):
        sql = """
            DELETE FROM fine
            WHERE id_fine=%s;
        """
        self._db.execute(sql, id_fine)

    def update(self, id_fine: int, reason: str, amount: float):
        sql = """
            UPDATE fine
            SET reason=%s, amount=%s
            WHERE id_fine=%s;
        """
        self._db.execute(sql, reason, amount, id_fine)
