from app.services import (
    AccessPolicy,
    AuthService,
    CassetteService,
    ClientService,
    ClientStatusService,
    EmployeeService,
    FineService,
    GenreService,
    PositionService,
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
    PositionRepository,
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
    PositionManagementPresenter,
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
    PositionManagementView,
    ProvisionConditionDialog,
    TariffManagementView,
    TariffTypeManagementView,
)

SECTIONS = {
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
    "ClientManagement": {
        "view": ClientManagementView,
        "presenter": "client_management",
    },
    "ClientStatusManagement": {
        "view": ClientStatusManagementView,
        "presenter": "status_management",
    },
    "EmployeeManagement": {
        "view": EmployeeManagementView,
        "presenter": "employee_management",
    },
    "PositionManagement": {
        "view": PositionManagementView,
        "presenter": "position_management",
    },
    "TariffTypeManagement": {
        "view": TariffTypeManagementView,
        "presenter": "tariff_type_management",
    },
    "TariffManagement": {
        "view": TariffManagementView,
        "presenter": "tariff_management",
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

        self.cassette_service = CassetteService(self.cassette_repo)
        self.genre_service = GenreService(self.genre_repo)
        self.auth_service = AuthService(self.employee_repo)
        self.fine_service = FineService(self.fine_repo)
        self.client_service = ClientService(self.client_repo)
        self.status_service = ClientStatusService(self.status_repo)
        self.position_service = PositionService(self.position_repo)
        self.employee_service = EmployeeService(self.employee_repo)
        self.tariff_type_service = TariffTypeService(self.tariff_type_repo)
        self.taiff_service = TariffService(self.taiff_repo)

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
            self.taiff_service,
            self.tariff_type_service,
            self.genre_service,
        )

    def main_window(self, employee) -> MainWindow:
        role = employee.position
        policy = AccessPolicy(role)

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
