from typing import Sequence

from .database import Database


class CassetteGenreData:

    def __init__(self, db: Database):
        self._db = db

    def list_for(self, id_cassette: int) -> Sequence[int]:
        sql = """
            SELECT id_genre
            FROM cassette_genre
            WHERE id_cassette=%s;
        """
        rows = self._db.fetch_all(sql, id_cassette)
        return [row[0] for row in rows]

    def replace(self, id_cassette: int, genres: Sequence[int]) -> None:
        sql = """
            DELETE FROM cassette_genre
            WHERE id_cassette=%s;
        """
        self._db.execute(sql, id_cassette)
        if genres:
            sql = """
                INSERT INTO cassette_genre (id_cassette, id_genre)
                VALUES (%s, %s);            
            """
            self._db.execute_many(
                sql, [(id_cassette, id_genre) for id_genre in genres]
            )
