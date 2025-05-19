from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Position


class PositionTableModel(QAbstractTableModel):
    _headers = ["ID", "Название", "Описание"]

    def __init__(self, rows: list[Position] | None = None):
        super().__init__()
        self._rows: list[Position] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        cs = self._rows[index.row()]
        return (cs.id_position, cs.name, cs.description)[index.column()]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[Position]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def position_id_at(self, row: int) -> int:
        return self._rows[row].id_position

    def position_at(self, row: int) -> Position:
        return self._rows[row]
