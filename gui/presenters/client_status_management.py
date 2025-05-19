from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import ClientStatusService
from gui.views import ClientStatusManagementView


class ClientStatusManagementPresenter(QObject):
    def __init__(self, view: ClientStatusManagementView, status_service: ClientStatusService):
        super().__init__()
        self._view = view
        self._status = status_service
        self._connect_signals()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.del_request.connect(self._on_del)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)

    @Slot(int)
    def _on_sel(self, id_status):
        try:
            status = self._status.get(id_status)
            if status:
                self._view.set_form(status)
        except Exception as e:
            self._show_err(e)

    @Slot(str, str)
    def _on_add(self, name, desc):
        try:
            self._status.add(name, desc)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int)
    def _on_del(self, id_status):
        try:
            self._status.delete(id_status)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str)
    def _on_upd(self, id_status, name, desc):
        try:
            self._status.update(id_status, name, desc)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    def _refresh(self):
        try:
            statuses = self._status.get_all()
            self._view.show_table(statuses)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)
