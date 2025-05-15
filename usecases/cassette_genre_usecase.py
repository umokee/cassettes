from dataclasses import dataclass
from typing import Sequence

from data import CassetteGenreData


@dataclass(slots=True)
class ListGenresForCassette:
    repo: CassetteGenreData

    def execute(self, id_cassette: int) -> None:
        return self.repo.list_for(id_cassette)


@dataclass(slots=True)
class SetCassetteGenres:
    repo: CassetteGenreData

    def execute(self, id_cassette: int, genres: Sequence[int]) -> None:
        self.repo.replace(id_cassette, genres)
