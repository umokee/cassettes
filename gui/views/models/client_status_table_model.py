from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import ClientStatus


class ClientStatusTableModel(QAbstractTableModel):
    _headers = ["ID", "Название", "Описание"]

    def __init__(self, rows: list[ClientStatus] | None = None):
        super().__init__()
        self._rows: list[ClientStatus] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        cs = self._rows[index.row()]
        return (cs.id_client_status, cs.name, cs.description)[index.column()]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[ClientStatus]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def status_id_at(self, row: int) -> int:
        return self._rows[row].id_client_status

    def status_at(self, row: int) -> ClientStatus:
        return self._rows[row]
