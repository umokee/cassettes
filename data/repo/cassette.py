from collections.abc import Sequence

from data import Database
from data.entities import Cassette


class CassetteRepository:
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
        result = []
        for row in rows:
            c = Cassette.from_row(row)
            c.genre_ids = self._load_genres_for(c.id_cassette)
            result.append(c)
        return result

    def list_available(self) -> Sequence[Cassette]:
        sql = """
            SELECT c.id_cassette,
                   c.title,
                   c.condition,
                   c.rental_cost,
                   COALESCE(string_agg(g.name, ', ' ORDER BY g.name), '') AS genres
            FROM cassette c
            LEFT JOIN cassette_genre cg ON cg.id_cassette = c.id_cassette
            LEFT JOIN genre         g  ON g.id_genre      = cg.id_genre
            LEFT JOIN rental        r  ON r.cassette_id_cassette = c.id_cassette
                                       AND r.rental_status = 'В процессе'
            WHERE r.id_rental IS NULL
            GROUP BY c.id_cassette
            ORDER BY c.id_cassette;
        """
        rows = self._db.fetch_all(sql)
        result = []
        for row in rows:                       # здесь уже 5 столбцов
            c = Cassette.from_row(row)
            c.genre_ids = self._load_genres_for(c.id_cassette)
            result.append(c)
        return result

    def get(self, id_cassette: int) -> Cassette | None:
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
        if not row:
            return None
        c = Cassette.from_row(row)
        c.genre_ids = self._load_genres_for(id_cassette)
        return c

    def add(self, title: str, cond: str, cost: float, genres: Sequence[int]):
        sql = """
            INSERT INTO cassette (title, condition, rental_cost)
            VALUES (%s, %s, %s)
            RETURNING id_cassette;
        """
        row = self._db.fetch_one(sql, title, cond, cost)
        if not row:
            raise RuntimeError("Ошибка при добавлении кассеты")
        id_cassette = int(row[0])
        self._save_genres(id_cassette, genres)

    def delete(self, id_cassette: int):
        sql = """
            DELETE FROM cassette_genre
            WHERE id_cassette=%s;
        """
        self._db.execute(sql, id_cassette)
        sql = """
            DELETE FROM cassette
            WHERE id_cassette=%s;
        """
        self._db.execute(sql, id_cassette)

    def update(
        self,
        id_cassette: int,
        title: str,
        cond: str,
        cost: float,
        genres: Sequence[int],
    ):
        sql = """
            UPDATE cassette
            SET title=%s, condition=%s, rental_cost=%s
            WHERE id_cassette=%s;
        """
        self._db.execute(sql, title, cond, cost, id_cassette)
        self._save_genres(id_cassette, genres)

    def _load_genres_for(self, id_cassette: int) -> Sequence[int]:
        sql = """
            SELECT id_genre
            FROM cassette_genre
            WHERE id_cassette=%s
        """
        rows = self._db.fetch_all(sql, id_cassette)
        return [row[0] for row in rows]

    def _save_genres(self, id_cassette: int, genres: Sequence[int]) -> None:
        sql = """
            DELETE FROM cassette_genre
            WHERE id_cassette=%s
        """
        self._db.execute(sql, id_cassette)
        if genres:
            sql = """
                INSERT INTO cassette_genre (id_cassette, id_genre)
                VALUES (%s, %s);
            """
            self._db.execute_many(sql, [(id_cassette, g) for g in genres])


    def _fetch_with_genres(self, sql: str, *params):
        """
        Выполняет запрос, затем подгружает genre_ids для каждой кассеты.
        """
        rows = self._db.fetch_all(sql, *params)
        result = []
        for row in rows:
            c = Cassette.from_row(row)
            c.genre_ids = self._load_genres_for(c.id_cassette)
            result.append(c)
        return result
