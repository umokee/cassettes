from .cassette import CassetteRepository
from .client import ClientRepository
from .client_status import ClientStatusRepository
from .employee import EmployeeRepository
from .fine import FineRepository
from .genre import GenreRepository
from .position import PositionRepository
from .tariff_type import TariffTypeRepository

__all__ = [
    "TariffTypeRepository",
    "PositionRepository",
    "ClientStatusRepository",
    "ClientRepository",
    "FineRepository",
    "CassetteRepository",
    "EmployeeRepository",
    "GenreRepository",
]
