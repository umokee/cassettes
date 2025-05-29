from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import (
    ClientService,
    FineService,
    PenaltyAccountingService,
    RentalService,
)
from gui.views import PenaltyAccountingView


class PenaltyAccountingPresenter(QObject):
    def __init__(
        self,
        view: PenaltyAccountingView,
        pa_svc: PenaltyAccountingService,
        client_svc: ClientService,
        rental_svc: RentalService,
        fine_svc: FineService,
    ):
        super().__init__()
        self._v = view
        self._pa = pa_svc
        self._clients = client_svc
        self._rentals = rental_svc
        self._fines = fine_svc

        self._v.client_cb.currentIndexChanged.connect(self._on_client_changed)
        self._v.accrue_request.connect(self._on_accrue)

        self._init_ui()

    def _init_ui(self):
        try:
            self._v.fill_clients(self._clients.get_all())
            self._on_client_changed()
        except Exception as e:
            self._show_err(e)

    def _refresh_table(self, client_id: int):
        fines = {f.id_fine: f.reason for f in self._fines.get_all()}
        self._v._model.set_lookups(fines)
        self._v.show_penalties(self._pa.list_by_client(client_id))

    @Slot()
    def _on_client_changed(self):
        cid = self._v.client_cb.currentData()
        if not cid:
            return
        try:
            self._v.fill_rentals(self._rentals.get_by_client(cid))
            self._v.fill_fines(self._fines.get_all())
            self._refresh_table(cid)
        except Exception as e:
            self._show_err(e)

    @Slot(int, int, list)
    def _on_accrue(self, _id_c: int, id_rental: int, fine_ids: list[int]):
        try:
            self._pa.accrue_fines(id_rental, fine_ids)
            QMessageBox.information(self._v, "Готово", "Штраф(ы) начислены")
            self._on_client_changed(_id_c)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._v, "Ошибка", str(e))
