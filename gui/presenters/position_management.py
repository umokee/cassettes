from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import PositionService
from gui.views import PositionManagementView


class PositionManagementPresenter(QObject):
    def __init__(self, view: PositionManagementView, position_service: PositionService):
        super().__init__()
        self._view = view
        self._position = position_service
        self._connect_signals()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.del_request.connect(self._on_del)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)

    @Slot(int)
    def _on_sel(self, id_position):
        try:
            position = self._position.get(id_position)
            if position:
                self._view.set_form(position)
        except Exception as e:
            self._show_err(e)

    @Slot(str, str)
    def _on_add(self, name, desc):
        try:
            self._position.add(name, desc)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int)
    def _on_del(self, id_position):
        try:
            self._position.delete(id_position)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str)
    def _on_upd(self, id_position, name, desc):
        try:
            self._position.update(id_position, name, desc)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    def _refresh(self):
        try:
            positions = self._position.get_all()
            self._view.show_table(positions)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)
