from .cassette import CassetteRepository
from .client import ClientRepository
from .client_status import ClientStatusRepository
from .employee import EmployeeRepository
from .fine import FineRepository
from .genre import GenreRepository

__all__ = [
    "ClientStatusRepository",
    "ClientRepository",
    "FineRepository",
    "CassetteRepository",
    "EmployeeRepository",
    "GenreRepository",
]
