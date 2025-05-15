from typing import Sequence

from base import BaseUseCase


class ListGenresForCassette(BaseUseCase):
    def perform(self, id_cassette: int) -> Sequence[int]:
        return self.repo.list_for(id_cassette)


class SetCassetteGenres(BaseUseCase):
    def perform(self, id_cassette: int, genres: Sequence[int]):
        self.repo.replace(id_cassette, genres)
