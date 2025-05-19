from collections.abc import Sequence
from contextlib import contextmanager
from typing import Any

import psycopg2

from app.config import DB_CONFIG


class Database:
    def __init__(self):
        self._conn = None
        self._connect()

    def _connect(self):
        try:
            self._conn = psycopg2.connect(**DB_CONFIG)
            self._conn.autocommit = False
        except Exception:
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @contextmanager
    def cursor(self):
        with self._conn.cursor() as cur:
            try:
                yield cur
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise

    def execute(self, sql: str, *params: Any):
        with self.cursor() as cur:
            cur.execute(sql, params)

    def execute_many(self, sql: str, seq: Sequence):
        with self.cursor() as cur:
            cur.executemany(sql, seq)

    def fetch_all(self, sql: str, *params: Any) -> list[tuple]:
        with self.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def fetch_one(self, sql: str, *params: Any) -> tuple | None:
        with self.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()

    def close(self):
        self._conn.close()
