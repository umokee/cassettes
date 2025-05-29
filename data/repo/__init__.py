from .cassette import CassetteRepository
from .client import ClientRepository
from .client_status import ClientStatusRepository
from .employee import EmployeeRepository
from .fine import FineRepository
from .genre import GenreRepository
from .penalty_accounting import PenaltyAccountingRepository
from .position import PositionRepository
from .rental import RentalRepository
from .tariff import TariffRepository
from .tariff_type import TariffTypeRepository

__all__ = [
    "PenaltyAccountingRepository",
    "RentalRepository",
    "TariffRepository",
    "TariffTypeRepository",
    "PositionRepository",
    "ClientStatusRepository",
    "ClientRepository",
    "FineRepository",
    "CassetteRepository",
    "EmployeeRepository",
    "GenreRepository",
]
