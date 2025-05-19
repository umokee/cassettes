from collections.abc import Sequence

from data import Database
from data.entities import Position


class PositionRepository:
    def __init__(self, db: Database):
        self._db = db

    def list(self) -> Sequence[Position]:
        sql = """
            SELECT id_position, name, description
            FROM position
            ORDER BY id_position;
        """
        rows = self._db.fetch_all(sql)
        return [Position.from_row(row) for row in rows]

    def get(self, id_position: int) -> Position | None:
        sql = """
            SELECT id_position, name, description
            FROM position
            WHERE id_position=%s;
        """
        row = self._db.fetch_one(sql, id_position)
        return Position.from_row(row) if row else None

    def add(self, name: str, description: str):
        sql = """
            INSERT INTO position (name, description)
            VALUES (%s, %s);
        """
        self._db.execute(sql, name, description)

    def delete(self, id_position: int):
        sql = """
            DELETE FROM position
            WHERE id_position=%s;
        """
        self._db.execute(sql, id_position)

    def update(self, id_position: int, name: str, desc: str):
        sql = """
            UPDATE position
            SET name=%s, description=%s
            WHERE id_position=%s;
        """
        self._db.execute(sql, name, desc, id_position)
