import re
from typing import Sequence

from base import BaseUseCase
from data import Cassette

_float_re = re.compile(r'^\d+(\.\d+)?$')


class ListCassettes(BaseUseCase):
    def perform(self) -> Sequence[Cassette]:
        return self.repo.list()


class AddCassette(BaseUseCase):
    def validate(self, title: str, _c: str, cost: str):
        title = (title or "").strip()
        cost_s = (cost or "").strip()

        if not title:
            raise ValueError("Заголовок не можешь быть пустым")
        if not cost_s:
            raise ValueError("Стоимость не может быть пустой")
        if not _float_re.match(cost_s):
            raise ValueError("Стоимость должна быть числом")
        if float(cost_s) < 0:
            raise ValueError("Стоимость не может быть меньше нуля")

    def perform(self, title: str, cond: str, cost: float) -> int:
        return self.repo.add_and_return_id(title, cond, float(cost))


class DeleteCassette(BaseUseCase):
    def perform(self, id_cassette: int):
        self.repo.delete(id_cassette)


class UpdateCassette(BaseUseCase):
    def validate(self, _i, title: str, _c, cost: str):
        title = (title or "").strip()
        cost_s = (cost or "").strip()

        if not title:
            raise ValueError("Заголовок не можешь быть пустым")
        if not cost_s:
            raise ValueError("Стоимость не может быть пустой")
        if not _float_re.match(cost_s):
            raise ValueError("Стоимость должна быть числом")
        if float(cost_s) < 0:
            raise ValueError("Стоимость не может быть меньше нуля")

    def perform(self, id_cassette: int, title: str, cond: str, cost: float):
        self.repo.update(id_cassette, title, cond, cost)
