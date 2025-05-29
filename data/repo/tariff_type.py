from collections.abc import Sequence

from data import Database
from data.entities import TariffType


class TariffTypeRepository:
    def __init__(self, db: Database):
        self._db = db

    def list(self) -> Sequence[TariffType]:
        sql = """
            SELECT
                id_tariff_type,
                name,
                description
            FROM tariff_type
            ORDER BY id_tariff_type;
        """
        rows = self._db.fetch_all(sql)
        return [TariffType.from_row(row) for row in rows]

    def get(self, id_tariff_type: int) -> TariffType | None:
        sql = """
            SELECT
                id_tariff_type,
                name,
                description
            FROM tariff_type
            WHERE id_tariff_type = %s;
        """
        row = self._db.fetch_one(sql, id_tariff_type)
        return TariffType.from_row(row) if row else None

    def add(self, name: str, description: str):
        sql = """
            INSERT INTO tariff_type (name, description)
            VALUES (%s, %s);
        """
        self._db.execute(sql, name, description)

    def delete(self, id_tariff_type: int):
        sql = """
            DELETE FROM tariff_type
            WHERE id_tariff_type=%s;
        """
        self._db.execute(sql, id_tariff_type)

    def update(self, id_tariff_type: int, name: str, desc: str):
        sql = """
            UPDATE tariff_type
            SET name = %s,
                description = %s
            WHERE id_tariff_type = %s;
        """
        self._db.execute(sql, name, desc, id_tariff_type)
