from typing import Optional, Sequence

from .database import Database
from .entity import Cassette


class CassetteData:

    def __init__(self, db: Database):
        self._db = db

    def list(self) -> Sequence[Cassette]:
        sql = """
            SELECT c.id_cassette, c.title, c.condition, c.rental_cost, 
            COALESCE(string_agg(g.name, ', ' ORDER BY g.name), '') AS genres
            FROM cassette c
            LEFT JOIN cassette_genre cg ON cg.id_cassette = c.id_cassette
            LEFT JOIN genre g ON g.id_genre = cg.id_genre
            GROUP BY c.id_cassette
            ORDER BY c.id_cassette;
        """
        rows = self._db.fetch_all(sql)
        return [Cassette(*row) for row in rows]

    def get(self, id_cassette: int) -> Optional[Cassette]:
        sql = """
            SELECT c.id_cassette, c.title, c.condition, c.rental_cost,
            COALESCE(string_agg(g.name, ', ' ORDER BY g.name), '') AS genres
            FROM cassette c
            LEFT JOIN cassette_genre cg ON cg.id_cassette = c.id_cassette
            LEFT JOIN genre g ON g.id_genre = cg.id_genre
            WHERE c.id_cassette=%s
            GROUP BY c.id_cassette;
        """
        row = self._db.fetch_one(sql, id_cassette)
        return Cassette(*row) if row else None

    def add(self, title: str, condition: str, rental_cost: float) -> None:
        sql = """
            INSERT INTO cassette (title, condition, rental_cost)
            VALUES (%s, %s, %s);
        """
        self._db.execute(sql, title, condition, rental_cost)

    def add_and_return_id(
        self, title: str, condition: str, rental_cost: float
    ) -> int:
        sql = """
            INSERT INTO cassette (title, condition, rental_cost)
            VALUES (%s, %s, %s)
            RETURNING id_cassette;
        """
        row = self._db.fetch_one(sql, title, condition, rental_cost)
        return int(row[0])

    def delete(self, id_cassette: int) -> None:
        sql = """
            DELETE FROM cassette
            WHERE id_cassette=%s;
        """
        self._db.execute(sql, id_cassette)

    def update(
        self, id_cassette: int, title: str, condition: str, rental_cost: float
    ) -> None:
        sql = """
            UPDATE cassette
            SET title=%s, condition=%s, rental_cost=%s
            WHERE id_cassette=%s;
        """
        self._db.execute(sql, title, condition, rental_cost, id_cassette)
