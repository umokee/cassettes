from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import Genre


class GenreTableModel(QAbstractTableModel):
    _headers = ["ID", "Name", "Description"]

    def __init__(self, rows: list[Genre] | None = None):
        super().__init__()
        self._rows: list[Genre] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        g = self._rows[index.row()]
        return (g.id_genre, g.name, g.description)[index.column()]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[Genre]) -> None:
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def genre_id_at(self, row: int) -> int:
        return self._rows[row].id_genre

    def genre_at(self, row: int) -> Genre:
        return self._rows[row]
