from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Fine


class FineTableModel(QAbstractTableModel):
    _headers = ["ID", "Причина", "Сумма"]

    def __init__(self, rows: list[Fine] | None = None):
        super().__init__()
        self._rows: list[Fine] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        f = self._rows[index.row()]
        return (f.id_fine, f.reason, f.amount)[index.column()]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[Fine]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def fine_id_at(self, row: int) -> int:
        return self._rows[row].id_fine

    def fine_at(self, row: int) -> Fine:
        return self._rows[row]
