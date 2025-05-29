from app.services import (
    AccessPolicy,
    AuthService,
    CassetteService,
    ClientService,
    ClientStatusService,
    EmployeeService,
    FineService,
    GenreService,
    PenaltyAccountingService,
    PositionService,
    RentalService,
    TariffService,
    TariffTypeService,
)
from data import Database
from data.repo import (
    CassetteRepository,
    ClientRepository,
    ClientStatusRepository,
    EmployeeRepository,
    FineRepository,
    GenreRepository,
    PenaltyAccountingRepository,
    PositionRepository,
    RentalRepository,
    TariffRepository,
    TariffTypeRepository,
)
from gui.presenters import (
    CassetteManagementPresenter,
    ClientManagementPresenter,
    ClientStatusManagementPresenter,
    EmployeeManagementPresenter,
    FineManagementPresenter,
    GenreManagementPresenter,
    PenaltyAccountingPresenter,
    PositionManagementPresenter,
    RentalManagementPresenter,
    TariffManagementPresenter,
    TariffTypeManagementPresenter,
)
from gui.views import (
    CassetteManagementView,
    ClientManagementView,
    ClientStatusManagementView,
    EmployeeManagementView,
    FineManagementView,
    GenreManagementView,
    MainWindow,
    PenaltyAccountingView,
    PositionManagementView,
    ProvisionConditionDialog,
    RentalManagementView,
    TariffManagementView,
    TariffTypeManagementView,
)

SECTIONS = {
    "RentalManagement": {
        "view": RentalManagementView,
        "presenter": "rental_management",
    },
    "PenaltyAccountingManagement": {
        "view": PenaltyAccountingView,
        "presenter": "penalty_management",
    },
    "CassetteManagement": {
        "view": CassetteManagementView,
        "presenter": "cassette_management",
    },
    "GenreManagement": {
        "view": GenreManagementView,
        "presenter": "genre_management",
    },
    "FineManagement": {
        "view": FineManagementView,
        "presenter": "fine_management",
    },
    "TariffManagement": {
        "view": TariffManagementView,
        "presenter": "tariff_management",
    },
    "ClientManagement": {
        "view": ClientManagementView,
        "presenter": "client_management",
    },
    "EmployeeManagement": {
        "view": EmployeeManagementView,
        "presenter": "employee_management",
    },
    "TariffTypeManagement": {
        "view": TariffTypeManagementView,
        "presenter": "tariff_type_management",
    },
    "ClientStatusManagement": {
        "view": ClientStatusManagementView,
        "presenter": "status_management",
    },
    "PositionManagement": {
        "view": PositionManagementView,
        "presenter": "position_management",
    },
}


class Container:
    def __init__(self):
        self.db = Database()
        self._build_services()

    def _build_services(self):
        self.cassette_repo = CassetteRepository(self.db)
        self.genre_repo = GenreRepository(self.db)
        self.employee_repo = EmployeeRepository(self.db)
        self.fine_repo = FineRepository(self.db)
        self.client_repo = ClientRepository(self.db)
        self.status_repo = ClientStatusRepository(self.db)
        self.position_repo = PositionRepository(self.db)
        self.tariff_type_repo = TariffTypeRepository(self.db)
        self.taiff_repo = TariffRepository(self.db)
        self.rental_repo = RentalRepository(self.db)
        self.penalty_repo = PenaltyAccountingRepository(self.db)

        self.cassette_service = CassetteService(self.cassette_repo)
        self.genre_service = GenreService(self.genre_repo)
        self.auth_service = AuthService(self.employee_repo)
        self.fine_service = FineService(self.fine_repo)
        self.client_service = ClientService(self.client_repo)
        self.status_service = ClientStatusService(self.status_repo)
        self.position_service = PositionService(self.position_repo)
        self.employee_service = EmployeeService(self.employee_repo)
        self.tariff_type_service = TariffTypeService(self.tariff_type_repo)
        self.tariff_service = TariffService(self.taiff_repo)
        self.rental_service = RentalService(self.rental_repo)
        self.penalty_service = PenaltyAccountingService(
            self.penalty_repo, self.fine_repo, self.rental_repo
        )

    def cassette_management(self, view: CassetteManagementView):
        return CassetteManagementPresenter(view, self.cassette_service, self.genre_service)

    def genre_management(self, view: GenreManagementView):
        return GenreManagementPresenter(view, self.genre_service)

    def fine_management(self, view: FineManagementView):
        return FineManagementPresenter(view, self.fine_service)

    def client_management(self, view: ClientManagementView):
        return ClientManagementPresenter(view, self.client_service, self.status_service)

    def status_management(self, view: ClientStatusManagementView):
        return ClientStatusManagementPresenter(view, self.status_service)

    def employee_management(self, view: EmployeeManagementView):
        return EmployeeManagementPresenter(view, self.employee_service, self.position_service)

    def position_management(self, view: PositionManagementView):
        return PositionManagementPresenter(view, self.position_service)

    def tariff_type_management(self, view: TariffTypeManagementView):
        return TariffTypeManagementPresenter(view, self.tariff_type_service)

    def tariff_management(self, view: TariffManagementView):
        return TariffManagementPresenter(
            view,
            ProvisionConditionDialog(),
            self.tariff_service,
            self.tariff_type_service,
            self.genre_service,
        )

    def rental_management(self, view: RentalManagementView):
        return RentalManagementPresenter(
            view,
            self.rental_service,
            self.client_service,
            self.cassette_service,
            self.tariff_service,
            self._current_employee.id_employee,
        )

    def penalty_management(self, view: PenaltyAccountingView):
        return PenaltyAccountingPresenter(
            view, self.penalty_service, self.client_service, self.rental_service, self.fine_service
        )

    def main_window(self, employee) -> MainWindow:
        self._current_employee = employee
        policy = AccessPolicy(employee.position)

        self.views = {}
        self.presenters = {}
        self.labels = {}

        for key, meta in SECTIONS.items():
            if not policy.is_enabled(key):
                continue

            view = meta["view"](readonly=policy.is_readonly(key))
            self.views[key] = view

            method = meta["presenter"]
            presenter = getattr(self, method)(view)
            self.presenters[key] = presenter

            self.labels[key] = policy.get_label(key)

        window = MainWindow(self.views, self.labels)
        window.set_current_employee(employee)
        return window

    def close(self):
        self.db.close()
