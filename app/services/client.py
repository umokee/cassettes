from collections.abc import Sequence

from data.entities import Client
from data.repo import ClientRepository


class ClientService:
    def __init__(self, repo: ClientRepository):
        self._repo = repo

    def get_all(self) -> Sequence[Client]:
        return self._repo.list()

    def add(self, full_name: str, login: str, email: str, id_status: int):
        self._validate(full_name, login, email)
        self._repo.add(full_name, login, email, id_status)

    def update(self, id_client: int, full_name: str, login: str, email: str, id_status: int):
        self._validate(full_name, login, email)
        self._repo.update(id_client, full_name, login, email, id_status)

    def change_password(self, id_client: int, new_password: str):
        self._repo.update_password(id_client, new_password)

    def _validate(self, full_name: str, login: str, email: str):
        if not full_name.strip():
            raise ValueError("ФИО не может быть пустым")
        if len(full_name) > 50:
            raise ValueError("ФИО слишком длинное (макс. 50 символов)")

        if not login.strip():
            raise ValueError("Логин не может быть пустым")
        if len(login) > 50:
            raise ValueError("Логин слишком длинный (макс. 50 символов)")

        if not email.strip():
            raise ValueError("Email не может быть пустым")
        if "@" not in email or "." not in email:
            raise ValueError("Некорректный email")
        if len(email) > 50:
            raise ValueError("Email слишком длинный (макс. 50 символов)")
