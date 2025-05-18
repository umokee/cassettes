from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ClientStatus:
    id_client_status: int
    name: str
    description: str

    @classmethod
    def from_row(cls, row: tuple[Any]) -> "ClientStatus":
        if len(row) == 3:
            return cls(*row)
        raise ValueError("Недопустимая строка для статуса клиента")
