from typing import Sequence

from base import BaseUseCase
from data import Genre


class ListGenres(BaseUseCase):
    def perform(self) -> Sequence[Genre]:
        return self.repo.list()


class AddGenre(BaseUseCase):
    def validate(self, name: str, _d):
        name = (name or "").strip()
        if not name:
            raise ValueError("Заголовок не можешь быть пустым")

    def perform(self, name: str, description: str):
        self.repo.add(name, description)


class DeleteGenre(BaseUseCase):
    def perform(self, id_genre: int):
        self.repo.delete(id_genre)


class UpdateGenre(BaseUseCase):
    def validate(self, _i, name: str, _d):
        name = (name or "").strip()
        if not name:
            raise ValueError("Заголовок не можешь быть пустым")

    def perform(self, id_genre: int, name: str, description: str):
        self.repo.update(id_genre, name, description)
