from collections.abc import Sequence

from data import Database
from data.entities import Tariff, TariffCondition


class TariffRepository:
    def __init__(self, db: Database):
        self._db = db

    def list(self) -> Sequence[Tariff]:
        sql = """
            SELECT
                t.id_tariff,
                t.name,
                t.coefficient,
                t.provision_conditions,
                tt.name
            FROM tariff t
            JOIN tariff_type tt
                ON tt.id_tariff_type = t.id_tariff_type
            ORDER BY t.id_tariff;
        """
        rows = self._db.fetch_all(sql)
        return [Tariff.from_row(row) for row in rows]

    def get(self, id_tariff: int) -> Tariff | None:
        sql = """
            SELECT
                t.id_tariff,
                t.name,
                t.coefficient,
                t.provision_conditions,
                tt.name
            FROM tariff t
            JOIN tariff_type tt
                ON tt.id_tariff_type = t.id_tariff_type
            WHERE t.id_tariff = %s;
        """
        row = self._db.fetch_one(sql, id_tariff)
        return Tariff.from_row(row) if row else None

    def add(self, name: str, coefficient: float, condition: TariffCondition, id_tariff_type: int):
        sql = """
            INSERT INTO tariff (name,
                                coefficient,
                                provision_conditions,
                                id_tariff_type)
            VALUES (%s, %s, %s, %s);
        """
        self._db.execute(sql, name, coefficient, condition.to_json(), id_tariff_type)

    def update(
        self,
        id_tariff: int,
        name: str,
        coefficient: float,
        condition: TariffCondition,
        id_tariff_type: int,
    ):
        sql = """
            UPDATE tariff
            SET name = %s,
                coefficient = %s,
                provision_conditions = %s,
                id_tariff_type = %s
            WHERE id_tariff = %s;
        """
        self._db.execute(sql, name, coefficient, condition.to_json(), id_tariff_type, id_tariff)

    def delete(self, id_tariff: int):
        sql = """
            DELETE FROM tariff
            WHERE id_tariff = %s;
        """
        self._db.execute(sql, id_tariff)
