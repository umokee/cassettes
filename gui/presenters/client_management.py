from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import ClientService, ClientStatusService
from gui.views import ClientManagementView


class ClientManagementPresenter(QObject):
    def __init__(
        self,
        view: ClientManagementView,
        client_service: ClientService,
        status_service: ClientStatusService,
    ):
        super().__init__()
        self._view = view
        self._client = client_service
        self._status = status_service
        self._connect_signals()
        self._init_statuses()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)

    def _init_statuses(self):
        if not self._view.is_readonly:
            try:
                statuses = self._status.get_all()
                self._view.set_statuses(statuses)
            except Exception as e:
                self._show_err(e)

    @Slot(int)
    def _on_sel(self, id_client):
        try:
            client = self._client.get(id_client)
            if client:
                self._view.set_form(client)
        except Exception as e:
            self._show_err(e)

    @Slot(str, str, str, int)
    def _on_add(self, full_name, login, email, id_status):
        try:
            self._client.add(full_name, login, email, id_status)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str, str, int)
    def _on_upd(self, id_client, full_name, login, email, id_status):
        try:
            self._client.update(id_client, full_name, login, email, id_status)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    def _refresh(self):
        try:
            clients = self._client.get_all()
            self._view.show_table(clients)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)
