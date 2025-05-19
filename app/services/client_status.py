from collections.abc import Sequence

from data.entities import ClientStatus
from data.repo import ClientStatusRepository


class ClientStatusService:
    def __init__(self, repo: ClientStatusRepository):
        self._repo = repo

    def get_all(self) -> Sequence[ClientStatus]:
        return self._repo.list()

    def get(self, id_status: int) -> ClientStatus | None:
        return self._repo.get(id_status)

    def add(self, name: str, desc: str):
        self._validate(name, desc)
        self._repo.add(name, desc)

    def update(self, id_client_status: int, name: str, desc: str):
        self._validate(name, desc)
        self._repo.update(id_client_status, name, desc)

    def delete(self, id_client_status: int):
        self._repo.delete(id_client_status)

    def _validate(self, name: str, desc: str):
        if not name.strip():
            raise ValueError("Название статуса не может быть пустым")
        if len(name) > 50:
            raise ValueError("Название статуса слишком длинное (макс. 50 символов)")

        if desc.strip() and len(desc) > 300:
            raise ValueError("Описание статуса слишком длинное (макс. 300 символов)")
