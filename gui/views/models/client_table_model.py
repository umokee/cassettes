from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Client


class ClientTableModel(QAbstractTableModel):
    _headers = ["ID", "ФИО", "Логин", "Email", "Статус"]

    def __init__(self, rows: list[Client] | None = None):
        super().__init__()
        self._rows: list[Client] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        c = self._rows[index.row()]
        return (c.id_client, c.full_name, c.login, c.email, c.status)[index.column()]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[Client]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def client_id_at(self, row: int) -> int:
        return self._rows[row].id_client

    def client_at(self, row: int) -> Client:
        return self._rows[row]
