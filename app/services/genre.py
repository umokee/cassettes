from collections.abc import Sequence

from data.entities import Genre
from data.repo import GenreRepository


class GenreService:
    def __init__(self, repo: GenreRepository):
        self._repo = repo

    def get_all(self) -> Sequence[Genre]:
        return self._repo.list()

    def get(self, id_genre: int) -> Genre | None:
        return self._repo.get(id_genre)

    def add(self, name: str, desc: str):
        self._validate(name, desc)
        self._repo.add(name, desc)

    def update(self, id_genre: int, name: str, desc: str):
        self._validate(name, desc)
        self._repo.update(id_genre, name, desc)

    def delete(self, id_genre: int):
        self._repo.delete(id_genre)

    def _validate(self, name: str, desc: str):
        if not name.strip():
            raise ValueError("Название жанра не может быть пустым")
        if len(name) > 50:
            raise ValueError("Название слишком длинное (макс. 50 символов)")

        if not desc.strip():
            raise ValueError("Описание жанра не может быть пустым")
        if len(desc) > 300:
            raise ValueError("Описание слишком длинное (макс. 300 символов)")
