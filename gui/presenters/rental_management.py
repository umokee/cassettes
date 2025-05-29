from datetime import date

from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import (
    CassetteService,
    ClientService,
    RentalService,
    TariffService,
)
from gui.views import RentalManagementView


class RentalManagementPresenter(QObject):
    def __init__(
        self,
        view: RentalManagementView,
        rental_svc: RentalService,
        client_svc: ClientService,
        cassette_svc: CassetteService,
        tariff_svc: TariffService,
        employee_id: int,
    ):
        super().__init__()
        self._v = view
        self._rentals = rental_svc
        self._clients = client_svc
        self._cassettes = cassette_svc
        self._tariffs = tariff_svc
        self._emp_id = employee_id

        self._connect_signals()
        self._fill_lists()
        self._refresh_table()

    def _connect_signals(self):
        self._v.opn_request.connect(self._on_open)
        self._v.cls_request.connect(self._on_close)
        self._v.cassette_input.currentIndexChanged.connect(self._on_cassette_changed)

    def _fill_lists(self):
        if self._v._readonly:
            return
        try:
            clients = self._clients.get_all()
            cassettes = self._cassettes.list_available()
            self._v.set_clients(clients)
            self._v.set_cassettes(cassettes)
            if cassettes:
                self._update_tariffs(cassettes[0].id_cassette)
        except Exception as e:
            self._show_err(e)

    def _refresh_table(self):
        try:
            rentals = self._rentals.get_active()
            cass_names = {c.id_cassette: c.title for c in self._cassettes.get_all()}
            client_names = {p.id_client: p.full_name for p in self._clients.get_all()}
            self._v.show_rentals(rentals, cass_names, client_names)
        except Exception as e:
            self._show_err(e)

    def _update_tariffs(self, cassette_id: int):
        try:
            cassette = self._cassettes.get(cassette_id)
            valid = self._tariffs.filter_for_cassette(cassette, date.today())
            self._v.set_tariffs(valid)
        except Exception as e:
            self._show_err(e)

    @Slot()
    def _on_cassette_changed(self):
        id_cassette = self._v.cassette_input.currentData()
        if id_cassette:
            self._update_tariffs(id_cassette)

    @Slot(int, int, int, int)
    def _on_open(self, id_client, id_cassette, id_tariff, days):
        try:
            cassette = self._cassettes.get(id_cassette)
            tariff = self._tariffs.get(id_tariff)
            cost = self._rentals.calc_cost(cassette, tariff, days)

            id_rental = self._rentals.open_rental(id_client, id_cassette, self._emp_id, days, cost)
            self._show_info("Успех", f"Аренда №{id_rental} оформлена")
            self._refresh_table()
            self._fill_lists()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str)
    def _on_close(self, id_rental, cond_after):
        try:
            self._rentals.close_rental(id_rental, self._emp_id, cond_after)
            self._show_info("Готово", "Возврат оформлен")
            self._refresh_table()
            self._fill_lists()
        except Exception as e:
            self._show_err(e)

    def _show_info(self, title: str, msg: str):
        QMessageBox.information(self._v, title, msg)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._v, "Ошибка", str(e), QMessageBox.StandardButton.Ok)
