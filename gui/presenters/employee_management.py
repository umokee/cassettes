from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QMessageBox

from app.services import EmployeeService, PositionService
from gui.views import EmployeeManagementView


class EmployeeManagementPresenter(QObject):
    def __init__(
        self,
        view: EmployeeManagementView,
        employee_service: EmployeeService,
        position_service: PositionService,
    ):
        super().__init__()
        self._view = view
        self._employee = employee_service
        self._position = position_service
        self._connect_signals()
        self._init_positions()
        self._refresh()

    def _connect_signals(self):
        self._view.add_request.connect(self._on_add)
        self._view.upd_request.connect(self._on_upd)
        self._view.sel_changed.connect(self._on_sel)

    def _init_positions(self):
        if not self._view.is_readonly:
            positions = self._position.get_all()
            self._view.set_positions(positions)

    @Slot(int)
    def _on_sel(self, id_employee):
        employee = next((e for e in self._employee.get_all() if e.id_employee == id_employee), None)
        if employee:
            self._view.set_form(employee)

    @Slot(str, str, str, str, int)
    def _on_add(self, full_name, login, passwd, email, id_status):
        try:
            self._employee.add(full_name, login, passwd, email, id_status)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    @Slot(int, str, str, str, str, int)
    def _on_upd(self, id_employee, full_name, login, passwd, email, id_status):
        try:
            self._employee.update(id_employee, full_name, login, passwd, email, id_status)
            self._refresh()
        except Exception as e:
            self._show_err(e)

    def _refresh(self):
        self._view.show_table(self._employee.get_all())

    def _show_err(self, exc: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(exc), QMessageBox.StandardButton.Ok)
