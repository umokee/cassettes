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
            try:
                positions = self._position.get_all()
                self._view.set_positions(positions)
            except Exception as e:
                self._show_err(e)

    @Slot(int)
    def _on_sel(self, id_employee):
        try:
            employee = self._employee.get(id_employee)
            if employee:
                self._view.set_form(employee)
        except Exception as e:
            self._show_err(e)

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
        try:
            employees = self._employee.get_all()
            self._view.show_table(employees)
        except Exception as e:
            self._show_err(e)

    def _show_err(self, e: Exception):
        QMessageBox.critical(self._view, "Ошибка", str(e), QMessageBox.StandardButton.Ok)
