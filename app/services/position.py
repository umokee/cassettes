from collections.abc import Sequence

from data.entities import Position
from data.repo import PositionRepository


class PositionService:
    def __init__(self, repo: PositionRepository):
        self._repo = repo

    def get_all(self) -> Sequence[Position]:
        return self._repo.list()

    def get(self, id_position: int) -> Position | None:
        return self._repo.get(id_position)

    def add(self, name: str, desc: str):
        self._validate(name, desc)
        self._repo.add(name, desc)

    def update(self, id_position: int, name: str, desc: str):
        self._validate(name, desc)
        self._repo.update(id_position, name, desc)

    def delete(self, id_position: int):
        self._repo.delete(id_position)

    def _validate(self, name: str, desc: str):
        if not name.strip():
            raise ValueError("Название статуса не может быть пустым")
        if len(name) > 50:
            raise ValueError("Название статуса слишком длинное (макс. 50 символов)")

        if desc.strip() and len(desc) > 300:
            raise ValueError("Описание статуса слишком длинное (макс. 300 символов)")
