from .cassette_management import CassetteManagementPresenter
from .client_management import ClientManagementPresenter
from .client_status_management import ClientStatusManagementPresenter
from .employee_management import EmployeeManagementPresenter
from .fine_management import FineManagementPresenter
from .genre_management import GenreManagementPresenter
from .penalty_management import PenaltyAccountingPresenter
from .position_management import PositionManagementPresenter
from .rental_management import RentalManagementPresenter
from .tariff_management import TariffManagementPresenter
from .tariff_type_management import TariffTypeManagementPresenter

__all__ = [
    "PenaltyAccountingPresenter",
    "RentalManagementPresenter",
    "TariffManagementPresenter",
    "TariffTypeManagementPresenter",
    "EmployeeManagementPresenter",
    "PositionManagementPresenter",
    "ClientManagementPresenter",
    "ClientStatusManagementPresenter",
    "FineManagementPresenter",
    "CassetteManagementPresenter",
    "GenreManagementPresenter",
]
