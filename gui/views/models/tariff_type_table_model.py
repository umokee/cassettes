from PySide6.QtCore import QAbstractTableModel, Qt

from data.entities import TariffType


class TariffTypeTableModel(QAbstractTableModel):
    _headers = ["ID", "Название", "Описание"]

    def __init__(self, rows: list[TariffType] | None = None):
        super().__init__()
        self._rows: list[TariffType] = rows or []

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        tt = self._rows[index.row()]
        return (tt.id_tariff_type, tt.name, tt.description)[index.column()]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def set_rows(self, rows: list[TariffType]):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def tariff_type_id_at(self, row: int) -> int:
        return self._rows[row].id_tariff_type

    def tariff_type_at(self, row: int) -> TariffType:
        return self._rows[row]
