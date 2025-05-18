import re
from collections.abc import Sequence

from data.entities import Fine
from data.repo import FineRepository


class FineService:
    def __init__(self, repo: FineRepository):
        self._repo = repo
        self._number_regex = re.compile(r"^\d+(\.\d+)?$")

    def get_all(self) -> Sequence[Fine]:
        return self._repo.list()

    def add(self, reason: str, amount: str):
        self._validate(reason, amount)
        self._repo.add(reason, float(amount))

    def update(self, id_fine: int, reason: str, amount: str):
        self._validate(reason, amount)
        self._repo.update(id_fine, reason, float(amount))

    def delete(self, id_fine: int):
        self._repo.delete(id_fine)

    def _validate(self, reason: str, amount: str):
        if not reason.strip():
            raise ValueError("Причина штрафа не может быть пустым")
        if len(reason) > 300:
            raise ValueError("Причина слишком длинная (макс. 300 символов)")

        if not self._number_regex.match(amount):
            raise ValueError("Сумма должна быть числом")
        if float(amount) <= 0:
            raise ValueError("Сумма должна быть положительной")
        if float(amount) >= 10_000:
            raise ValueError("Сумма слишком большая")
