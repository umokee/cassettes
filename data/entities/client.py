from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Client:
    id_client: int
    full_name: str
    login: str
    password: str
    email: str
    status: str

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "Client":
        if len(row) == 6:
            return cls(*row)
        raise ValueError("Недопустимая строка для клиента")
