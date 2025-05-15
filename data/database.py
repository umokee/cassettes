from contextlib import contextmanager
from typing import Any, Sequence

import psycopg2

dsn = "dbname=Cassettes user=postgres password=112211 host=192.168.1.118"


class Database:

    def __init__(self, autocommmit: bool = False):
        self._conn = psycopg2.connect(dsn)
        self._conn.autocommit = autocommmit

    @contextmanager
    def cursor(self):
        with self._conn.cursor() as cur:
            try:
                yield cur
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise

    def execute(self, sql: str, *params: Any) -> None:
        with self.cursor() as cur:
            cur.execute(sql, params)

    def execute_many(self, sql: str, seq: Sequence) -> None:
        with self.cursor() as cur:
            cur.executemany(sql, seq)

    def fetch_all(self, sql: str, *params: Any) -> list[tuple]:
        with self.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def fetch_one(self, sql: str, *params: Any) -> tuple | None:
        rows = self.fetch_all(sql, *params)
        return rows[0] if rows else None

    def close(self) -> None:
        self._conn.close()
