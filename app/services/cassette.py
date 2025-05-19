import re
from collections.abc import Sequence

from data.entities import Cassette
from data.repo import CassetteRepository


class CassetteService:
    def __init__(self, repo: CassetteRepository):
        self._repo = repo
        self._number_regex = re.compile(r"^\d+(\.\d+)?$")

    def get_all(self) -> Sequence[Cassette]:
        return self._repo.list()

    def get(self, id_cassette: int) -> Cassette | None:
        return self._repo.get(id_cassette)

    def add(self, title: str, cond: str, cost: str, genres: list[int]):
        self._validate(title, cost)
        self._repo.add(title, cond, float(cost), genres)

    def update(self, id_cassette: int, title: str, cond: str, cost: str, genres: list[int]):
        self._validate(title, cost)
        self._repo.update(id_cassette, title, cond, float(cost), genres)

    def delete(self, id_cassette: int):
        self._repo.delete(id_cassette)

    def _validate(self, title: str, cost: str):
        if not title.strip():
            raise ValueError("Название кассеты не может быть пустым")
        if len(title.strip()) > 50:
            raise ValueError("Название слишком длинное (макс. 50 символов)")

        if not self._number_regex.match(cost):
            raise ValueError("Стоимость должна быть числом")
        if float(cost) <= 0:
            raise ValueError("Стоимость должна быть положительной")
        if float(cost) >= 10_000:
            raise ValueError("Стоимость слишком большая")
