from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Employee


class EmployeeTableModel(QAbstractTableModel):
    _headers = ["ID", "ФИО", "Логин", "Пароль", "Email", "Должность"]

    def __init__(self, rows: list[Employee] | None = None):
        super().__init__()
        self._rows: list[Employee] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        e = self._rows[index.row()]
        return (e.id_employee, e.full_name, e.login, e.password, e.email, e.position)[
            index.column()
        ]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[Employee]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def employee_id_at(self, row: int) -> int:
        return self._rows[row].id_employee

    def employee_at(self, row: int) -> Employee:
        return self._rows[row]
