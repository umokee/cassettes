from dataclasses import dataclass
from typing import Sequence

from data import Genre, GenreData


@dataclass(slots=True)
class ListGenres:
    repo: GenreData

    def execute(self) -> Sequence[Genre]:
        return self.repo.list()


@dataclass(slots=True)
class AddGenre:
    repo: GenreData

    def execute(self, name: str, description: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("Title cannot be empty")
        self.repo.add(name, description)


@dataclass(slots=True)
class DeleteGenre:
    repo: GenreData

    def execute(self, id_genre: int) -> None:
        self.repo.delete(id_genre)


@dataclass(slots=True)
class UpdateGenre:
    repo: GenreData

    def execute(self, id_genre: int, name: str, description: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("Title cannot be empty")
        self.repo.update(id_genre, name, description)
