from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import TariffTypeService
from gui.views import TariffTypeManagementView


class TariffTypeManagementPresenter(QObject):
    def __init__(self, view: TariffTypeManagementView, type_service: TariffTypeService):
        super().__init__()
        self._view = view
        self._type = type_service
        self._connect_signals()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.del_request.connect(self._on_del)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)

    @Slot(int)
    def _on_sel(self, id_type):
        try:
            type = self._type.get(id_type)
            if type:
                self._view.set_form(type)
        except Exception as e:
            self._show_err(e)

    @Slot(str, str)
    def _on_add(self, name, desc):
        try:
            self._type.add(name, desc)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int)
    def _on_del(self, id_type):
        try:
            self._type.delete(id_type)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str)
    def _on_upd(self, id_type, name, desc):
        try:
            self._type.update(id_type, name, desc)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    def _refresh(self):
        try:
            types = self._type.get_all()
            self._view.show_table(types)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)
