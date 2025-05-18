from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Cassette


class CassetteTableModel(QAbstractTableModel):
    _headers = ["ID", "Title", "Condition", "Rental cost", "Genres"]

    def __init__(self, rows: list[Cassette] | None = None):
        super().__init__()
        self._rows: list[Cassette] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        c = self._rows[index.row()]
        return (c.id_cassette, c.title, c.condition, c.rental_cost, c.genres)[index.column()]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[Cassette]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def cassette_id_at(self, row: int) -> int:
        return self._rows[row].id_cassette

    def cassette_at(self, row: int) -> Cassette:
        return self._rows[row]
