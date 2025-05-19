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

        self._bind()
        self._fill_lists()
        self._refresh_table()

    # ---------- util ----------
    def _bind(self):
        self._v.open_request.connect(self._on_open)
        self._v.close_request.connect(self._on_close)
        self._v.cassette_cb.currentIndexChanged.connect(self._on_cassette_changed)

    def _fill_lists(self):
        self._v.fill_clients(self._clients.get_all())
        free = self._cassettes.list_available()
        self._v.fill_cassettes(free)
        if free:
            self._update_tariffs(free[0].id_cassette)

    def _refresh_table(self):
        self._v.show_rentals(self._rentals.list_open())

    def _update_tariffs(self, cassette_id: int):
        cass = self._cassettes.get(cassette_id)
        today = date.today()

        valid = []
        for t in self._tariffs.get_all():
            c = t.provision_condition
            if c.genres and not (set(c.genres) & set(cass.genre_ids)):
                continue
            if c.weekdays and today.isoweekday() not in c.weekdays:
                continue
            if c.dates and not (c.dates.start <= str(today) <= c.dates.end):
                continue
            valid.append(t)
        self._v.fill_tariffs(valid)

    # ---------- slots ----------
    @Slot()
    def _on_cassette_changed(self):
        cid = self._v.cassette_cb.currentData()
        if cid:
            self._update_tariffs(cid)

    @Slot(int, int, int, int)
    def _on_open(self, id_client, id_cassette, id_tariff, days):
        try:
            cassette = self._cassettes.get(id_cassette)
            tariff = self._tariffs.get(id_tariff)
            cost = cassette.rental_cost * tariff.coefficient * days

            rid = self._rentals.open_rental(id_client, id_cassette, self._emp_id, days, cost)
            QMessageBox.information(self._v, "Успех", f"Аренда №{rid} оформлена")
            self._refresh_table()
        except Exception as e:
            QMessageBox.critical(self._v, "Ошибка", str(e))

    @Slot(int, str)
    def _on_close(self, id_rental, cond_after):
        try:
            self._rentals.close_rental(id_rental, self._emp_id, cond_after)
            QMessageBox.information(self._v, "Готово", "Возврат оформлен")
            self._refresh_table()
        except Exception as e:
            QMessageBox.critical(self._v, "Ошибка", str(e))
