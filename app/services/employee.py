from collections.abc import Sequence

from data.entities import Employee
from data.repo import EmployeeRepository


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self._repo = repo

    def get_all(self) -> Sequence[Employee]:
        return self._repo.list()

    def get(self, id_employee: int) -> Employee | None:
        return self._repo.get(id_employee)

    def add(self, full_name: str, login: str, password: str, email: str, id_position: int):
        self._validate(full_name, login, password, email)
        self._repo.add(full_name, login, password, email, id_position)

    def update(
        self,
        id_client: int,
        full_name: str,
        login: str,
        password: str,
        email: str,
        id_position: int,
    ):
        self._validate(full_name, login, password, email)
        self._repo.update(id_client, full_name, login, password, email, id_position)

    def _validate(self, full_name: str, login: str, password: str, email: str):
        if not full_name.strip():
            raise ValueError("ФИО не может быть пустым")
        if len(full_name) > 50:
            raise ValueError("ФИО слишком длинное (макс. 50 символов)")

        if not login.strip():
            raise ValueError("Логин не может быть пустым")
        if len(login) > 50:
            raise ValueError("Логин слишком длинный (макс. 50 символов)")

        if not password.strip():
            raise ValueError("Пароль не может быть пустым")
        if len(password) > 50:
            raise ValueError("Пароль слишком длинный (макс. 50 символов)")

        if not email.strip():
            raise ValueError("Email не может быть пустым")
        if "@" not in email or "." not in email:
            raise ValueError("Некорректный email")
        if len(email) > 100:
            raise ValueError("Email слишком длинный (макс. 100 символов)")
