from collections.abc import Sequence

from data import Database
from data.entities import Genre


class GenreRepository:
    def __init__(self, db: Database):
        self._db = db

    def list(self) -> Sequence[Genre]:
        sql = """
            SELECT
                id_genre,
                name,
                description
            FROM genre
            ORDER BY id_genre;
        """
        rows = self._db.fetch_all(sql)
        return [Genre.from_row(row) for row in rows]

    def get(self, id_genre: int) -> Genre | None:
        sql = """
            SELECT
                id_genre,
                name,
                description
            FROM genre
            WHERE id_genre = %s;
        """
        row = self._db.fetch_one(sql, id_genre)
        return Genre.from_row(row) if row else None

    def add(self, name: str, description: str):
        sql = """
            INSERT INTO genre (name, description)
            VALUES (%s, %s);
        """
        self._db.execute(sql, name, description)

    def delete(self, id_genre: int):
        sql = """
            DELETE FROM genre
            WHERE id_genre = %s;
        """
        self._db.execute(sql, id_genre)

    def update(self, id_genre: int, name: str, desc: str):
        sql = """
            UPDATE genre
            SET name = %s,
                description = %s
            WHERE id_genre = %s;
        """
        self._db.execute(sql, name, desc, id_genre)
