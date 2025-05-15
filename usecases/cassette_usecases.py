from dataclasses import dataclass
from typing import Sequence

from data import Cassette, CassetteData, CassetteGenreData

@dataclass(slots=True)
class ListCassettes:
    repo: CassetteData

    def execute(self) -> Sequence[Cassette]:
        return self.repo.list()


@dataclass(slots=True)
class _Validator:
    @staticmethod
    def check(title: str, rental_cost: float) -> None:
        if not title.strip():
            raise ValueError("Заголовок не можешь быть пустым")
        if rental_cost < 0:
            raise ValueError("Стоимость не может быть меньше нуля")


@dataclass(slots=True)
class AddCassette:
    repo: CassetteData

    def execute(self, title: str, cond: str, cost: float) -> None:
        _Validator.check(title, cost)
        return self.repo.add_and_return_id(title, cond, cost)


@dataclass(slots=True)
class DeleteCassette:
    repo: CassetteData

    def execute(self, id_cassette: int) -> None:
        self.repo.delete(id_cassette)


@dataclass(slots=True)
class UpdateCassette:
    repo: CassetteData

    def execute(
        self, id_cassette: int, title: str, cond: str, cost: float
    ) -> None:
        _Validator.check(title, cost)
        self.repo.update(id_cassette, title, cond, cost)
