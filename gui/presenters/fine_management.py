from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import FineService
from gui.views import FineManagementView


class FineManagementPresenter(QObject):
    def __init__(self, view: FineManagementView, fine_service: FineService):
        super().__init__()
        self._view = view
        self._fine = fine_service
        self._connect_signals()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.del_request.connect(self._on_del)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)

    @Slot(int)
    def _on_sel(self, id_fine):
        try:
            fine = self._fine.get(id_fine)
            if fine:
                self._view.set_form(fine)
        except Exception as e:
            self._show_err(e)

    @Slot(str, str)
    def _on_add(self, reason, amount):
        try:
            self._fine.add(reason, amount)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int)
    def _on_del(self, id_fine):
        try:
            self._fine.delete(id_fine)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str)
    def _on_upd(self, id_fine, reason, amount):
        try:
            self._fine.update(id_fine, reason, amount)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    def _refresh(self):
        try:
            fines = self._fine.get_all()
            self._view.show_table(fines)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)
