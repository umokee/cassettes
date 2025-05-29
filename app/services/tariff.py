import re
from collections.abc import Sequence
from datetime import date

from data.entities import Cassette, Tariff, TariffCondition
from data.repo import TariffRepository


class TariffService:
    def __init__(self, repo: TariffRepository):
        self._repo = repo
        self._number_regex = re.compile(r"^\d+(\.\d+)?$")

    def get_all(self) -> Sequence[Tariff]:
        return self._repo.list()

    def get(self, id_tariff: int) -> Tariff | None:
        return self._repo.get(id_tariff)

    def filter_for_cassette(
        self,
        cassette: Cassette,
        today: date | None = None,
    ) -> Sequence[Tariff]:
        today = today or date.today()
        res: list[Tariff] = []
        for t in self._repo.list():
            c = t.provision_condition
            if c.genres and not (set(c.genres) & set(cassette.genre_ids)):
                continue
            if c.weekdays and today.isoweekday() not in c.weekdays:
                continue
            if c.dates and not (c.dates.start <= str(today) <= c.dates.end):
                continue
            res.append(t)
        return res

    def add(self, name: str, coefficient: str, cond: TariffCondition, id_tariff_type: int):
        self._validate(name, coefficient)
        self._repo.add(name, float(coefficient), cond, id_tariff_type)

    def update(
        self,
        id_tariff: int,
        name: str,
        coeff: str,
        cond: TariffCondition,
        id_type: int,
    ):
        self._validate(name, coeff)
        self._repo.update(id_tariff, name, float(coeff), cond, id_type)

    def delete(self, id_tariff: int):
        self._repo.delete(id_tariff)

    def _validate(self, name: str, coefficient: str):
        if not name.strip():
            raise ValueError("Название тарифа не может быть пустым")
        if len(name.strip()) > 50:
            raise ValueError("Название тарифа слишком длинное (макс. 50 символов)")

        if not self._number_regex.match(coefficient):
            raise ValueError("Коэффициент должен быть числом")
        if float(coefficient) <= 0:
            raise ValueError("Коэффициент должен быть положительным")
        if float(coefficient) > 1:
            raise ValueError("Коэффициент слишком большой (макс. 1.00)")
